#!/usr/bin/env python3
"""Lookup an item value from the items.json data file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lookup the value of an item from items.json"
    )
    parser.add_argument(
        "item_name",
        metavar="ITEM",
        help="Name of the item whose value should be returned",
    )
    return parser.parse_args()


def load_items(file_path: Path) -> dict[str, object]:
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise SystemExit(
            f"Could not find {file_path}. Please ensure the data file exists."
        ) from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Failed to decode JSON in {file_path}: {exc.msg} (line {exc.lineno})"
        ) from exc


def main() -> None:
    args = parse_args()
    items_path = Path(__file__).with_name("items.json")
    items = load_items(items_path)

    try:
        value = items[args.item_name]
    except KeyError as exc:
        raise SystemExit(
            f"Item '{args.item_name}' was not found in {items_path}."
        ) from exc

    if isinstance(value, (dict, list)):
        json.dump(value, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(value)


if __name__ == "__main__":
    main()
