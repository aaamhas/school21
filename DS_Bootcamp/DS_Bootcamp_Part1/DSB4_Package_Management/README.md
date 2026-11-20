# DSB4 · Python Package Management

Четвёртый проект первой части DS Bootcamp Школы 21. Шесть упражнений посвящены виртуальным окружениям, установке пакетов, терминальным диаграммам, разбору HTML, профилированию и тестированию.

## Упражнения

| Упражнение | Тема | Файлы |
| --- | --- | --- |
| 00 | Определение активного виртуального окружения | [`venv.py`](src/ex00/venv.py) |
| 01 | Диаграммы в терминале с termgraph | [`pies_bars.sh`](src/ex01/pies_bars.sh), [`data.txt`](src/ex01/data.txt) |
| 02 | Установка библиотек и сохранение списка зависимостей | [`librarian.py`](src/ex02/librarian.py), [`requirements.txt`](src/ex02/requirements.txt), [архив окружения](src/ex02/karlondo.tar.gz) |
| 03 | Получение финансовых показателей Yahoo Finance через Requests и BeautifulSoup | [`financial.py`](src/ex03/financial.py) |
| 04 | Сравнение вариантов с Requests и HTTPX, анализ времени и числа вызовов | [`financial.py`](src/ex04/financial.py), [`financial_enhanced.py`](src/ex04/financial_enhanced.py), [`pstat.py`](src/ex04/pstat.py) |
| 05 | Проверка парсера с pytest | [`financial.py`](src/ex05/financial.py), [`financial_test.py`](src/ex05/financial_test.py) |

## Подготовка

Нужен Python 3. Создайте окружение из папки проекта.

```sh
python -m venv .venv
```

Активируйте его командой `.venv\Scripts\Activate.ps1` в PowerShell или `source .venv/bin/activate` в Bash на Linux и macOS.

Сохранённый список зависимостей относится к учебному окружению. Для запуска финансовых скриптов дополнительно нужны `requests` и `httpx`.

```sh
python -m pip install -r src/ex02/requirements.txt
python -m pip install requests httpx
```

## Примеры запуска

Из папки проекта проверьте активное окружение.

```sh
python src/ex00/venv.py
```

Для диаграммы перейдите в `src/ex01` и выполните `bash pies_bars.sh` в Bash с активным Python-окружением. Скрипт читает `data.txt` и строит диаграмму с двумя рядами данных.

Финансовый скрипт принимает тикер компании и название показателя.

```sh
python src/ex03/financial.py MSFT "Total Revenue"
python src/ex04/financial.py MSFT "Total Revenue"
python src/ex04/financial_enhanced.py MSFT "Total Revenue"
```

Результат — кортеж с названием показателя и значениями из строки таблицы Yahoo Finance. В версиях из упражнений 03 и 05 после HTTP-запроса предусмотрена пауза в пять секунд.

## Профилирование

В `src/ex04` сохранены результаты исходных измерений.

| Файл | Содержание |
| --- | --- |
| [`profiling-sleep.txt`](src/ex04/profiling-sleep.txt) | Профиль варианта с искусственной задержкой |
| [`profiling-tottime.txt`](src/ex04/profiling-tottime.txt) | Профиль без задержки с сортировкой по внутреннему времени |
| [`profiling-http.txt`](src/ex04/profiling-http.txt) | Профиль варианта с HTTPX |
| [`profiling-ncalls.txt`](src/ex04/profiling-ncalls.txt) | Статистика по числу вызовов |
| [`pstats-cumulative.txt`](src/ex04/pstats-cumulative.txt) | Пять строк профиля с наибольшим накопленным временем |
| [`profile_output.prof`](src/ex04/profile_output.prof) | Сохранённый бинарный профиль |

Для нового измерения перейдите в `src/ex04` и выполните команды.

```sh
python -m cProfile -o profile_output.prof financial.py MSFT "Total Revenue"
python pstat.py
```

`pstat.py` читает `profile_output.prof` и записывает статистику в `pstats-cumulative.txt`.

## Тесты и особенности исходников

Для запуска семи исходных тестов перейдите в `src/ex05`.

```sh
python -m pytest financial_test.py -v
```

Тесты обращаются к Yahoo Finance и зависят от доступности сайта и его текущей HTML-разметки.

В `src/ex02/librarian.py` на строке 9 есть исходная ошибка отступа `IndentationError: unexpected indent`. Она препятствует запуску упражнения 02. Зависимости можно установить приведёнными выше командами `pip`.

[Вернуться к списку проектов](../../../README.md)
