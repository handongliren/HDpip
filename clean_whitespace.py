import pathlib

root = pathlib.Path(__file__).resolve().parent

for py in root.rglob("*.py"):
    lines = py.read_text(encoding = "utf-8").splitlines()

    # 清理行尾空格
    cleaned = [line.rstrip() for line in lines]

    # 空行去重：连续空行只保留一个
    deduped = []
    prev_blank = False
    for line in cleaned:
        if line == "":
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False
        deduped.append(line)

    if deduped != lines:
        py.write_text("\n".join(deduped) + "\n", encoding = "utf-8")
        print(f"已清理: {py}")
