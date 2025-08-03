import argparse
import shutil
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def parse_args():
    parser = argparse.ArgumentParser(description="Багатопотокове сортування файлів за розширеннями.")
    parser.add_argument("source", type=Path, help="Шлях до вихідної директорії з файлами.")
    parser.add_argument("--output", type=Path, default=Path("dist"),
                        help="Шлях до директорії для відсортованих файлів (за замовчуванням: dist).")
    return parser.parse_args()


def copy_file(source_path: Path, output_dir: Path):
    try:
        extension = source_path.suffix[1:].lower() if source_path.suffix else "no_extension"

        target_dir = output_dir / extension
        target_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy(source_path, target_dir)
        logging.info(f"Скопійовано {source_path} до {target_dir}")
    except Exception as e:
        logging.error(f"Не вдалося скопіювати {source_path}. Помилка: {e}")


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    args = parse_args()
    source_dir = args.source
    output_dir = args.output

    if not source_dir.is_dir():
        logging.error(f"Вихідна директорія не існує або не є директорією: {source_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Цільова директорія: {output_dir}")
    logging.info("Починаємо сканування вихідної директорії...")
    try:
        files_to_copy = [item for item in source_dir.rglob('*') if item.is_file()]
        logging.info(f"Знайдено {len(files_to_copy)} файлів для копіювання.")
    except Exception as e:
        logging.error(f"Помилка під час сканування директорії {source_dir}: {e}")
        return
    with ThreadPoolExecutor(max_workers=10) as executor:
        for file_path in files_to_copy:
            executor.submit(copy_file, file_path, output_dir)

    logging.info("Сортування завершено.")


if __name__ == "__main__":
    main()
