import io
import pathlib
import tokenize

def _spaceEquals(text: str) -> str:
    lines = text.splitlines(keepends = True)
    line_offsets = [0]
    for line in lines:
        line_offsets.append(line_offsets[-1] + len(line))

    edits = []
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type != tokenize.OP or token.string != "=":
            continue
        token_offset = line_offsets[token.start[0] - 1] + token.start[1]
        left = token_offset
        while left > 0 and text[left - 1] in " \t":
            left -= 1
        right = token_offset + 1
        while right < len(text) and text[right] in " \t":
            right += 1
        if text[left:token_offset] != " ":
            edits.append((left, token_offset, " "))
        if text[token_offset + 1:right] != " ":
            edits.append((token_offset + 1, right, " "))

    for start, end, replacement in sorted(edits, reverse = True):
        text = text[:start] + replacement + text[end:]
    return text

root = pathlib.Path(__file__).resolve().parent
skip_dirs = {"build", "dist", "site", ".git", "__pycache__", ".venv", "hdpip.egg-info"}

def main() -> None:
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

        result = _spaceEquals(newline.join(deduped) + newline)
        if result != text:
            with py.open("w", encoding = "utf-8", newline = "") as f:
                f.write(result)
            print(f"已清理: {py}")

if __name__ == "__main__":
    main()
