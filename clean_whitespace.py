import ast
import io
import pathlib
import tokenize

def _argumentEquals(text: str) -> set[int]:
    lines = text.splitlines(keepends = True)
    if not lines:
        return set()
    tree = ast.parse(text)
    line_offsets = [0]
    for line in lines:
        line_offsets.append(line_offsets[-1] + len(line))

    def offset(line: int, column: int) -> int:
        byte_column = len(lines[line - 1].encode("utf-8")[:column].decode("utf-8"))
        return line_offsets[line - 1] + byte_column

    argument_ranges = []

    def addArgumentDefaults(arguments: ast.arguments) -> None:
        positional = arguments.posonlyargs + arguments.args
        if arguments.defaults:
            for argument, default in zip(positional[-len(arguments.defaults):], arguments.defaults):
                argument_ranges.append((
                    offset(argument.end_lineno, argument.end_col_offset), 
                    offset(default.lineno, default.col_offset), 
                ))
        for argument, default in zip(arguments.kwonlyargs, arguments.kw_defaults):
            if default is not None:
                argument_ranges.append((
                    offset(argument.end_lineno, argument.end_col_offset), 
                    offset(default.lineno, default.col_offset), 
                ))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            addArgumentDefaults(node.args)
        if isinstance(node, (ast.Call, ast.ClassDef)):
            for keyword in node.keywords:
                if keyword.arg is not None:
                    argument_ranges.append((
                        offset(keyword.lineno, keyword.col_offset), 
                        offset(keyword.value.lineno, keyword.value.col_offset), 
                    ))
        elif isinstance(node, ast.Assign):
            targets = node.targets
            for left, right in zip(targets, targets[1:] + [node.value]):
                argument_ranges.append((
                    offset(left.end_lineno, left.end_col_offset), 
                    offset(right.lineno, right.col_offset), 
                ))
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            left = node.annotation if node.annotation is not None else node.target
            argument_ranges.append((
                offset(left.end_lineno, left.end_col_offset), 
                offset(node.value.lineno, node.value.col_offset), 
            ))

    equals = set()
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type != tokenize.OP or token.string != "=":
            continue
        token_offset = line_offsets[token.start[0] - 1] + token.start[1]
        if any(start <= token_offset < end for start, end in argument_ranges):
            equals.add(token_offset)
    return equals

def _spaceArgumentEquals(text: str) -> str:
    edits = []
    for equals in _argumentEquals(text):
        left = equals
        while left > 0 and text[left - 1] in " \t":
            left -= 1
        right = equals + 1
        while right < len(text) and text[right] in " \t":
            right += 1
        if text[left:equals] != " ":
            edits.append((left, equals, " "))
        if text[equals + 1:right] != " ":
            edits.append((equals + 1, right, " "))

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

        result = _spaceArgumentEquals(newline.join(deduped) + newline)
        if result != text:
            with py.open("w", encoding = "utf-8", newline = "") as f:
                f.write(result)
            print(f"已清理: {py}")

if __name__ == "__main__":
    main()
