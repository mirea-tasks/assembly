# Пример входного файла:
```
[
    {
        "op": "LOAD_CONST",
        "value": 915
    },
    {
        "op": "LOAD_MEM",
        "offset": 260
    },
    {
        "op": "STORE_MEM"
    },
    {
        "op": "ABS"
    }
]
```

## Описание формата:
- op: Операция, которая будет выполнена (например, LOAD_CONST, LOAD_MEM).
- value: Значение, которое загружается в память или стек (для операций типа LOAD_CONST).
- offset: Смещение для операций чтения/записи из памяти (для операций типа LOAD_MEM и STORE_MEM).

## Запуск
- ```python main.py program.json test.json --test```