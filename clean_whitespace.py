import pathlib

root = pathlib.Path(__file__).resolve().parent
skip_dirs = {"build", "dist", "site", ".git", "__pycache__", ".venv", "hdpip.egg-info"}

for py in root.rglob("*.py"):
    if any(part in skip_dirs for part in py.relative_to(root).parts):
        continue

    text = py.open(encoding = "utf-8", newline = "").read()
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(newline)
    if lines and lines[-1] == "":
        lines = lines[:-1]

    # 清理行尾空格，行尾英文逗号后自动补一个空格
    cleaned = [line.rstrip() + " " if line.rstrip().endswith(",") else line.rstrip() for line in lines]

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

    result = newline.join(deduped) + newline
    if result != text:
        with py.open("w", encoding = "utf-8", newline = "") as f:
            f.write(result)
        print(f"已清理: {py}")
