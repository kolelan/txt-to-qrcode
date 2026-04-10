import argparse
from pathlib import Path
from typing import Iterable

import qrcode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Преобразует файл(ы) с текстом в QR-коды PNG."
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Путь к файлу или папке для обработки.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Папка для вывода PNG. При указании сохраняется структура входных данных."
        ),
    )
    return parser.parse_args()


def iter_files(input_path: Path) -> Iterable[Path]:
    if input_path.is_file():
        yield input_path
        return

    for item in input_path.rglob("*"):
        if item.is_file():
            yield item


def read_text_any(file_path: Path) -> str:
    data = file_path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def qr_name_for(source_file: Path) -> str:
    return f"{source_file.name.replace('.', '_')}.png"


def output_path_for(source_file: Path, input_root: Path, output_root: Path | None) -> Path:
    if output_root is None:
        return source_file.with_name(qr_name_for(source_file))

    if input_root.is_file():
        rel_parent = Path()
    else:
        rel_parent = source_file.parent.relative_to(input_root)

    return output_root / rel_parent / qr_name_for(source_file)


def make_qr(text: str, out_file: Path) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    img = qrcode.make(text)
    img.save(out_file)


def main() -> None:
    args = parse_args()
    input_path: Path = args.input_path
    output_root: Path | None = args.output

    if not input_path.exists():
        raise FileNotFoundError(f"Путь не найден: {input_path}")
    if output_root is not None:
        output_root.mkdir(parents=True, exist_ok=True)

    files = list(iter_files(input_path))
    if not files:
        print("Файлы для обработки не найдены.")
        return

    created = 0
    for src in files:
        try:
            text = read_text_any(src)
            out_file = output_path_for(src, input_path, output_root)
            make_qr(text, out_file)
            print(f"OK: {src} -> {out_file}")
            created += 1
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: {src} ({exc})")

    print(f"Готово. Создано QR-кодов: {created}")


if __name__ == "__main__":
    main()
