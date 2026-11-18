# DSB3 · Python OOP Skills

Третий проект первой части DS Bootcamp Школы 21. Семь упражнений последовательно развивают программу анализа подбрасываний монеты — от простого класса до модулей, текстового отчёта, логирования и уведомлений в Telegram.

## Упражнения

| Упражнение | Тема | Реализация |
| --- | --- | --- |
| 00 | Класс и чтение файла | [`first_class.py`](src/ex00/first_class.py) |
| 01 | Метод экземпляра класса | [`first_method.py`](src/ex01/first_method.py) |
| 02 | Конструктор, путь к файлу и проверка данных | [`first_constructor.py`](src/ex02/first_constructor.py) |
| 03 | Вложенный класс, подсчёт исходов и их долей | [`first_nest.py`](src/ex03/first_nest.py) |
| 04 | Наследование и генерация случайных прогнозов | [`first_child.py`](src/ex04/first_child.py) |
| 05 | Разделение на модули, конфигурация и сохранение отчёта | [`analytics.py`](src/ex05/analytics.py), [`config.py`](src/ex05/config.py), [`make_report.py`](src/ex05/make_report.py) |
| 06 | Логирование и Telegram-уведомления о результате | [`analytics.py`](src/ex06/analytics.py), [`config.example.py`](src/ex06/config.example.py), [`make_report.py`](src/ex06/make_report.py) |

## Данные

В каждом упражнении есть `data.csv` с заголовком `head,tail` и 11 наблюдениями. Строки `1,0` и `0,1` обозначают два исхода подбрасывания монеты. Метод чтения в упражнениях 02–06 проверяет формат входных данных.

В упражнениях 05 и 06 сохранены примеры отчёта `file.txt`. Случайная часть прогноза меняется при повторном запуске. Количество будущих наблюдений задаёт `num_of_steps` в конфигурации.

## Запуск

Нужен Python 3. Проверено на Python 3.13.7. Для упражнений 00–05 достаточно стандартной библиотеки, упражнение 06 использует `requests`.

Запускайте каждое упражнение из его каталога. Из папки проекта можно выполнить команды ниже.

```sh
(cd src/ex00 && python first_class.py)
(cd src/ex01 && python first_method.py)
(cd src/ex02 && python first_constructor.py data.csv)
(cd src/ex03 && python first_nest.py data.csv)
(cd src/ex04 && python first_child.py data.csv)
(cd src/ex05 && python make_report.py)
```

В PowerShell перейдите в нужный каталог командой `cd` и выполните соответствующую команду `python`.

`make_report.py` из упражнения 05 записывает отчёт в `src/ex05/file.txt`.

## Telegram и логирование

Файл `src/ex06/config.example.py` содержит шаблон конфигурации с пустыми `token` и `chat_id`. Создайте рабочую копию в каталоге упражнения.

```sh
cd src/ex06
python -c "from shutil import copyfile; copyfile('config.example.py', 'config.py')"
python -m pip install requests
```

Заполните `token` и `chat_id` в созданном `config.py` данными своего Telegram-бота и чата, затем выполните команду.

```sh
python make_report.py
```

Программа записывает отчёт в `file.txt`, журнал в `analytics.log` и отправляет в Telegram уведомление об успешном создании отчёта или обработанной ошибке. Рабочий `src/ex06/config.py` исключён из Git.

Дополнительный `src/ex06/test.py` отправляет тестовое сообщение в настроенный Telegram-чат при запуске.

[Вернуться к списку проектов](../../../README.md)
