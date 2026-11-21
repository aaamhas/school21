# DSB5 · Efficient Code Practices

Пятый проект первой части DS Bootcamp Школы 21. Шесть упражнений сравнивают способы обработки коллекций и файлов по времени выполнения и потреблению памяти.

## Упражнения

| Упражнение | Тема | Реализация |
| --- | --- | --- |
| 00 | Цикл и списковое включение | [`benchmark.py`](src/ex00/benchmark.py) |
| 01 | Добавление реализации с `map` | [`benchmark.py`](src/ex01/benchmark.py) |
| 02 | Сравнение `loop`, `list_comprehension`, `map` и `filter` через аргументы командной строки | [`benchmark.py`](src/ex02/benchmark.py) |
| 03 | Сумма квадратов с циклом и `functools.reduce` | [`benchmark.py`](src/ex03/benchmark.py) |
| 04 | Частоты и десять наиболее частых значений с собственными функциями и `collections.Counter` | [`benchmark.py`](src/ex04/benchmark.py) |
| 05 | Чтение файла в список и построчное чтение через генератор | [`ordinary.py`](src/ex05/ordinary.py), [`generator.py`](src/ex05/generator.py) |

## Подготовка

Упражнения 00–04 используют стандартную библиотеку Python. Для упражнения 05 нужен `psutil`.

```sh
python -m pip install psutil
```

Проверено на Python 3.13.7 в Windows. Измерение пиковой памяти в упражнении 05 использует Windows-поле `peak_wset` из `psutil`.

## Бенчмарки коллекций

Все команды ниже выполняются из папки проекта.

```sh
python src/ex00/benchmark.py
python src/ex01/benchmark.py
```

Эти скрипты выполняют по 9000 повторений каждой реализации. В упражнениях 01 и 02 `map_method` оставляет `None` на местах адресов с другим почтовым доменом.

Упражнение 02 принимает название функции и число повторений.

```sh
python src/ex02/benchmark.py loop 1000
python src/ex02/benchmark.py list_comprehension 1000
python src/ex02/benchmark.py map 1000
python src/ex02/benchmark.py filter 1000
```

Упражнение 03 принимает название функции, число повторений и положительную верхнюю границу суммы квадратов.

```sh
python src/ex03/benchmark.py loop 1000 1000
python src/ex03/benchmark.py reduce 1000 1000
```

Упражнение 04 создаёт миллион случайных целых чисел от 0 до 100 и сравнивает подсчёт частот и поиск наиболее частых значений.

```sh
python src/ex04/benchmark.py
```

Скрипты выводят результаты измерений `timeit` в секундах.

## Список и генератор на MovieLens

Для упражнения 05 используется `ratings.csv` из MovieLens 25M.

1. Скачайте архив `ml-25m.zip` с официальной страницы GroupLens.
2. Распакуйте архив и поместите `ml-25m/ratings.csv` в `src/ex05/ratings.csv`.
3. Запустите оба скрипта отдельными процессами.

[MovieLens 25M и ссылка на архив](https://grouplens.org/datasets/movielens/25m/)

```sh
python src/ex05/ordinary.py src/ex05/ratings.csv
python src/ex05/generator.py src/ex05/ratings.csv
```

`ordinary.py` загружает строки в список через `readlines()`. `generator.py` читает файл построчно с помощью `yield`. Оба скрипта выводят пиковое потребление памяти в гигабайтах и суммарное процессорное время в секундах.

Файл `ratings.csv` занимает около 678 МБ и исключён из Git. Скрипты также принимают путь к другому CSV-файлу.

[Вернуться к списку проектов](../../../README.md)
