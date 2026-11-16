# DSB1 · UNIX Command Line Tools

Первый проект DS Bootcamp Школы 21. Набор POSIX shell-скриптов обрабатывает выборку из 20 вакансий HeadHunter. Проект охватывает преобразование JSON в CSV, сортировку, выделение грейдов, агрегацию и разбиение данных по датам.

## Упражнения

| Этап | Что делает | Файлы |
| --- | --- | --- |
| 00 · Данные | Использует сохранённую выборку вакансий | [`hh.json`](src/ex00/hh.json) |
| 01 · JSON → CSV | Извлекает ID, дату, название, признак тестового задания и ссылку | [`filter.jq`](src/ex01/filter.jq), [`json_to_csv.sh`](src/ex01/json_to_csv.sh), [CSV](src/ex01/hh.csv) |
| 02 · Сортировка | Сортирует вакансии по времени публикации | [`sorter.sh`](src/ex02/sorter.sh), [CSV](src/ex02/hh_sorted.csv) |
| 03 · Очистка | Оставляет в названии грейды `Junior`, `Middle` и `Senior`, если они указаны | [`cleaner.sh`](src/ex03/cleaner.sh), [CSV](src/ex03/hh_positions.csv) |
| 04 · Агрегация | Считает повторения значений выбранного поля | [`counter.sh`](src/ex04/counter.sh), [сохранённая сводка](src/ex04/hh_uniq_positions.csv) |
| 05 · Разбиение и сборка | Разбивает строки по датам публикации и собирает обратно в один CSV | [`partitioner.sh`](src/ex05/partitioner.sh), [`concatenator.sh`](src/ex05/concatenator.sh), [CSV](src/ex05/hh_concatenated.csv) |

## Как запустить

Понадобятся `sh`, `jq`, GNU Awk под именем `awk` и стандартные UNIX-утилиты. Выборка уже в репозитории, поэтому токен HeadHunter и подключение к API не нужны.

Выполните из папки проекта. Команды создают временную копию `src`, чтобы проверочный запуск сохранял исходные CSV.

```sh
scratch="$(mktemp -d)"
cp -R src "$scratch/"
rm -f "$scratch"/src/ex05/*.csv

(cd "$scratch/src/ex01" && sh json_to_csv.sh)
(cd "$scratch/src/ex02" && sh sorter.sh)
(cd "$scratch/src/ex03" && sh cleaner.sh)
(cd "$scratch/src/ex04" && sh counter.sh)
(cd "$scratch/src/ex05" && sh partitioner.sh && sh concatenator.sh)

cmp "$scratch/src/ex03/hh_positions.csv" "$scratch/src/ex05/hh_concatenated.csv"
printf 'Результаты: %s\n' "$scratch/src"
```

## Сохранённые результаты

Сохранённая сводка упражнения 04 содержит 10 вакансий без явного грейда, 8 с `Junior`, по одной с `Middle` и `Senior`. При новом запуске исходный `counter.sh` считает значения второго поля `created_at`. Из-за этого свежая сводка отличается от сохранённой.

Для упражнения 05 нужен чистый каталог срезов. `concatenator.sh` читает все `*.csv` в своём каталоге, включая итоговый файл от предыдущего запуска. Команды выше удаляют старые CSV только из временной копии.
