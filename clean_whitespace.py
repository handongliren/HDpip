import pathlib

root = pathlib.Path(__file__).resolve().parent

for py in root.rglob("*.py"):
    lines = py.read_text(encoding = "utf-8").splitlines()
    cleaned = [line.rstrip() for line in lines]
    if cleaned != lines:
        py.write_text("\n".join(cleaned) + "\n", encoding = "utf-8")
        print(f"已清理: {py}")
