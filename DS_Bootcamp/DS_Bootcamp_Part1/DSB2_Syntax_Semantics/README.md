# DSB2 · Python Syntax and Semantics

Второй проект первой части DS Bootcamp Школы 21. Десять упражнений знакомят с типами данных Python, файлами, словарями, множествами, строками и аргументами командной строки.

## Упражнения

| Упражнение | Тема | Реализация |
| --- | --- | --- |
| 00 | Базовые типы данных и их названия | [`data_types.py`](src/ex00/data_types.py) |
| 01 | Преобразование CSV в TSV с учётом запятых внутри кавычек | [`read_and_write.py`](src/ex01/read_and_write.py) |
| 02 | Поиск цены по названию компании | [`stock_prices.py`](src/ex02/stock_prices.py) |
| 03 | Поиск компании и цены по тикеру | [`ticker_symbols.py`](src/ex03/ticker_symbols.py) |
| 04 | Преобразование списка пар в словарь с группировкой значений | [`to_dictionary.py`](src/ex04/to_dictionary.py) |
| 05 | Обработка списка названий компаний и тикеров | [`all_stocks.py`](src/ex05/all_stocks.py) |
| 06 | Сортировка словаря по числовому значению и названию | [`dict_sorter.py`](src/ex06/dict_sorter.py) |
| 07 | Операции над множествами для сегментации клиентов | [`marketing.py`](src/ex07/marketing.py) |
| 08 | Извлечение имён из адресов электронной почты и персональное приветствие | [`names_extractor.py`](src/ex08/names_extractor.py), [`letter_starter.py`](src/ex08/letter_starter.py) |
| 09 | Кодирование и декодирование текста шифром Цезаря | [`caesar.py`](src/ex09/caesar.py) |

## Запуск

Нужен Python 3. Проверено на Python 3.13.7. Все скрипты используют стандартную библиотеку.

Команды ниже выполняются из папки проекта.

```sh
python src/ex00/data_types.py
python src/ex02/stock_prices.py apple
python src/ex03/ticker_symbols.py aapl
python src/ex04/to_dictionary.py
python src/ex05/all_stocks.py "apple, MSFT, unknown"
python src/ex06/dict_sorter.py
python src/ex07/marketing.py call_center
python src/ex09/caesar.py encode "Hello, World!" 3
python src/ex09/caesar.py decode "Khoor, Zruog!" 3
```

`stock_prices.py apple` выводит `287.73`, а `ticker_symbols.py aapl` — `Apple 287.73`. Цены заданы в учебных словарях внутри скриптов.

У `marketing.py` также есть режимы `potential_clients` и `loyalty_program`. Порядок элементов множества в выводе может различаться.

Шифр Цезаря сохраняет регистр латинских букв и знаки препинания. Для примера выше результат кодирования — `Khoor, Zruog!`. Кириллица вызывает предусмотренную в скрипте ошибку.

## Упражнения с файлами

Для упражнений 01 и 08 текущим каталогом должна быть папка соответствующего упражнения. Скрипты обращаются к файлам по относительным путям.

```sh
cd src/ex01
python read_and_write.py
```

`read_and_write.py` читает сохранённый `ds.csv` из 20 записей и записывает результат в `ds.tsv`.

Для упражнения 08 перейдите в `src/ex08` и выполните команду.

```sh
python names_extractor.py adresses.txt
```

Скрипт создаёт `employees.tsv` с колонками `Name`, `Surname` и `E-mail`. Файл `adresses.txt` уже содержит учебные примеры. Для приветствия передайте `letter_starter.py` адрес из колонки `E-mail`.

```sh
python letter_starter.py "<адрес из employees.tsv>"
```

[Вернуться к списку проектов](../../../README.md)
