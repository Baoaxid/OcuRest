import csv
import json
import os
import re
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "csv"
OUTPUT_DIR = BASE_DIR / "locales"

def extract_key_columns(headers: list) -> list:
    key_cols = [h for h in headers if re.match(r"^key\d+$", h)]
    return sorted(key_cols, key=lambda x: int(x[3:]))

def validate_keys(keys: list) -> Optional[str]:
    found_empty = False
    has_value = False
    for key in keys:
        if not key:
            found_empty = True
        else:
            has_value = True
            if found_empty:
                return "gap_in_keys"
    return None if has_value else "no_keys"

def set_deep(target: dict, keys: list, value: str, meta: dict) -> None:
    current = target
    for idx, key in enumerate(keys):
        if idx == len(keys) - 1:
            if key in current and current[key] != value:
                meta["overwrites"].append({
                    "path": ".".join(keys),
                    "old_value": current[key],
                    "new_value": value,
                    "line": meta["line"],
                    "locale": meta["locale"]
                })
            current[key] = value
        else:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

def process_file(file_path: Path) -> dict:
    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            raw_headers = next(reader)
        except StopIteration:
            return {"file": file_path.stem, "invalid_rows": [], "overwrites": []}

    headers = [h.strip() for h in raw_headers]
    key_columns = extract_key_columns(headers)
    locale_columns = [h for h in headers if h not in key_columns]

    if not key_columns or not locale_columns:
        raise ValueError(f"Invalid columns schema in {file_path}")

    results = {loc: {} for loc in locale_columns}
    invalid_rows = []
    overwrites = []

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as f:
        dict_reader = csv.DictReader(f)
        for idx, row in enumerate(dict_reader):
            line_number = idx + 2
            keys = [row.get(k, "").strip() for k in key_columns]

            error = validate_keys(keys)
            if error:
                invalid_rows.append({"line": line_number, "reason": error, "keys": keys})
                continue

            filtered_keys = [k for k in keys if k]
            for loc in locale_columns:
                raw_val = row.get(loc, "")
                if raw_val is None:
                    continue
                val = raw_val.strip().replace("\\n", "\n")
                if not val:
                    continue
                meta = {"overwrites": overwrites, "line": line_number, "locale": loc}
                set_deep(results[loc], filtered_keys, val, meta)

    base_name = file_path.stem
    for loc, data in results.items():
        loc_dir = OUTPUT_DIR / loc
        loc_dir.mkdir(parents=True, exist_ok=True)
        with open(loc_dir / f"{base_name}.json", "w", encoding="utf-8") as out:
            json.dump(data, out, ensure_ascii=False, indent=2)

    return {"file": base_name, "invalid_rows": invalid_rows, "overwrites": overwrites}

def main():
    if not INPUT_DIR.exists():
        print(f"Directory not found: {INPUT_DIR}")
        return

    csv_files = list(INPUT_DIR.glob("*.csv"))
    for f in csv_files:
        print(f"Compiling: {f.name}")
        report = process_file(f)
        if report["invalid_rows"]:
            print(f"Invalid rows detected in {f.name}: {len(report['invalid_rows'])}")
        if report["overwrites"]:
            print(f"Overwrites detected in {f.name}: {len(report['overwrites'])}")

    print("Localization compilation completed successfully.")

if __name__ == "__main__":
    main()
