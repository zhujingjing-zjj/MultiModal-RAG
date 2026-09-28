import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _is_abs_path(s: str) -> bool:
    return bool(re.match(r"^[A-Za-z]:[\\/]", s)) or s.startswith("\\\\")


def _basename(p: str) -> str:
    p = p.replace("\\", "/")
    return p.rsplit("/", 1)[-1]


def normalize_data_check_json(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for _, item in data.items():
        if not isinstance(item, dict):
            continue
        key = "图片地址"
        if key not in item or not isinstance(item[key], str):
            continue
        value = item[key]
        if _is_abs_path(value) or "/" in value or "\\" in value:
            item[key] = _basename(value)
            changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
    return changed


def normalize_dataset_data_test_json(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    def walk(x):
        nonlocal changed
        if isinstance(x, dict):
            for k, v in list(x.items()):
                if isinstance(v, str):
                    x[k] = normalize_string(v)
                else:
                    walk(v)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                if isinstance(v, str):
                    x[i] = normalize_string(v)
                else:
                    walk(v)

    def normalize_string(s: str) -> str:
        nonlocal changed
        # e.g. data:image/jpeg;base64,E:/.../1-1.jpg  -> data:image/jpeg;base64,1-1.jpg
        m = re.search(r"(data:image/[^;]+;base64,)([A-Za-z]:[\\/][^\"\\s]+)", s)
        if m:
            changed = True
            return m.group(1) + _basename(m.group(2))
        return s

    walk(data)
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
    return changed


def main() -> None:
    targets = [
        ROOT / "data_check.json",
        ROOT / "dataset" / "data_check.json",
        ROOT / "dataset" / "data_test.json",
    ]

    for p in targets:
        if not p.exists():
            continue
        if p.name == "data_test.json":
            did = normalize_dataset_data_test_json(p)
        else:
            did = normalize_data_check_json(p)
        print(f"{p.relative_to(ROOT)}: {'updated' if did else 'ok'}")


if __name__ == "__main__":
    main()

