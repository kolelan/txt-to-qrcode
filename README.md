# txt-to-qrcode

Скрипт `txt_to_qrcode.py` преобразует содержимое файла (или набора файлов в папке) в QR-коды PNG.

## Возможности

- На вход подается файл или папка.
- Для папки обработка идет рекурсивно по всем файлам.
- Любой файл пытается прочитаться как текст:
  - `utf-8`
  - `utf-8-sig`
  - `cp1251`
  - `latin-1`
  - fallback: `utf-8` с `errors="replace"`
- Имя выходного PNG строится из полного имени файла:
  - точки `.` заменяются на `_`
  - в конец добавляется `.png`
- С `--output` создается зеркальная структура папок и файлы QR складываются туда.
- Без `--output` QR создаются рядом с исходными файлами.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Использование

### 1) Один файл

```bash
python txt_to_qrcode.py "example\wifi_password.txt"
```

Создаст файл `example\wifi_password_txt.png`.

### 2) Папка рекурсивно

```bash
python txt_to_qrcode.py "example"
```

Создаст PNG рядом с каждым найденным файлом внутри `example`.

### 3) Папка с отдельным каталогом вывода

```bash
python txt_to_qrcode.py "example" --output "out"
```

В `out` будет создана структура, повторяющая `example`, а внутри — PNG-файлы QR.

## Демонстрационные входные файлы

В проекте есть папка `example` с тремя файлами на разных уровнях:

- `example\wifi_password.txt`
- `example\network\wg_tunnel.conf`
- `example\certs\ssl\service.crt`

Каждый из них можно обработать отдельно или вместе через папку `example`.
