#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import argparse
from pathlib import Path


def show_tree(dir, level, m_level, files, hidden, sizes):
    def format_size(size):
        # Конвертация размера до читаемого состояния
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f}{unit}"
            size /= 1024
        return f"{size:.2f}PB"

    def tree(dir_path, prefix=""):
        if m_level is not None and level[0] >= m_level:
            return
        level[0] += 1

        contents = sorted(list(dir_path.iterdir()), key=lambda p: p.is_file())
        for count, path in enumerate(contents):
            if not hidden and path.name.startswith("."):
                continue

            connector = "└── " if count == len(contents) - 1 else "├── "
            size_info = (
                f" ({format_size(path.stat().st_size)})"
                if sizes and path.is_file()
                else ""
            )
            print(f"{prefix}{connector}{path.name}{size_info}")

            if path.is_dir():
                extension = "    " if count == len(contents) - 1 else "│   "
                tree(path, prefix + extension)

        level[0] -= 1

    start_path = Path(dir).expanduser()
    if not start_path.exists():
        print(f"Каталог '{dir}' не существует")
        return

    print(start_path)
    tree(start_path)


def main():
    parser = argparse.ArgumentParser(
        description="Показать дерево каталогов"
    )
    parser.add_argument(
        "dir", nargs="?", default=".", help="Показать каталог"
    )
    parser.add_argument(
        "-l", "--level", type=int, help="Уйти вниз по каталогам"
    )
    parser.add_argument(
        "-f", "--files", action="store_true", help="Показать файлы в каталоге"
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="Показать скрытые файлы"
    )
    parser.add_argument("-s", "--sizes", action="store_true", help="Показать размеры файлов")
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        help="Показать счетчик каталогов и файлов",
    )

    args = parser.parse_args()

    if args.count:
        count(args.dir)
    else:
        show_tree(args.dir, [0], args.level, args.files, args.all, args.sizes)


def count(directory):
    files = 0
    dirs = 0

    for root, dirs, files in os.walk(directory):
        dirs += len(dirs)
        files += len(files)

    print(f"Всего каталогов: {dirs}")
    print(f"Всего файлов: {files}")


if __name__ == "__main__":
    main()