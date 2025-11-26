import argparse
import json

from dataclasses import dataclass
from typing import List, Optional


INSTRUCTION_SPECS = {
    "LOAD_CONST": {
        "A": 26,
        "has_B": True,
        "B_name": "value",
        "B_bits": 27,
    },
    "LOAD_MEM": {
        "A": 47,
        "has_B": True,
        "B_name": "offset",
        "B_bits": 12,
    },
    "STORE_MEM": {
        "A": 25,
        "has_B": False,
    },
    "ABS": {
        "A": 40,
        "has_B": False,
    },
}


@dataclass
class IRInstruction:
    mnemonic: str  # имя команды: LOAD_CONST / LOAD_MEM / STORE_MEM / ABS
    A: int  # поле A (опкод)
    B: Optional[int] = None  # поле B, если есть

    def to_fields_repr(self) -> str:
        if self.B is None:
            return f"A={self.A}"
        return f"A={self.A}, B={self.B}"


def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--test", action="store_true", default=False)
    return parser.parse_args()


def load_source_program(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Исходная программа в JSON должна быть списком объектов.")

    return data


def assemble_to_ir(ast: List[dict]) -> List[IRInstruction]:
    ir: List[IRInstruction] = []

    for idx, node in enumerate(ast):
        if not isinstance(node, dict):
            raise ValueError(f"Инструкция #{idx} не является JSON-объектом.")

        if "op" not in node:
            raise ValueError(f"Инструкция #{idx} не содержит поле 'op'.")

        mnemonic = node["op"]
        if mnemonic not in INSTRUCTION_SPECS:
            raise ValueError(f"Неизвестная команда '{mnemonic}' в инструкции #{idx}.")

        spec = INSTRUCTION_SPECS[mnemonic]
        A = spec["A"]

        if spec.get("has_B", False):
            b_name = spec.get("B_name", "B")
            if b_name not in node:
                raise ValueError(
                    f"Инструкция #{idx} '{mnemonic}' должна содержать аргумент '{b_name}'."
                )
            B = int(node[b_name])

            if "B_bits" in spec:
                max_val = (1 << spec["B_bits"]) - 1
                if not (0 <= B <= max_val):
                    raise ValueError(
                        f"Инструкция #{idx}: значение {b_name}={B} "
                        f"не помещается в {spec['B_bits']} бит (0..{max_val})."
                    )
        else:
            B = None

        ir.append(IRInstruction(mnemonic=mnemonic, A=A, B=B))

    return ir


def print_ir_for_test(ir: List[IRInstruction]) -> None:
    print("IR:")
    for i, instr in enumerate(ir):
        print(f"{i:03d}: {instr.mnemonic}: {instr.to_fields_repr()}")


def save_ir_as_json(ir: List[IRInstruction], path: str) -> None:
    data = []
    for instr in ir:
        obj = {
            "mnemonic": instr.mnemonic,
            "A": instr.A,
        }
        if instr.B is not None:
            obj["B"] = instr.B
        data.append(obj)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    args = parse_cli_args()
    ast = load_source_program(args.source)
    ir = assemble_to_ir(ast)

    if args.test:
        print_ir_for_test(ir)

    save_ir_as_json(ir, args.output)


if __name__ == "__main__":
    main()
