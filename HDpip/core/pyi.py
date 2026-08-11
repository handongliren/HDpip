"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于生成.pyi文件。
"""

import ast
import pathlib
import shutil
import traceback

# 存根中保留的装饰器（其余丢弃，如 @override）
_KEEP_DECORATORS = {"overload", "classmethod", "staticmethod", "property", "abstractmethod", "final"}

def getDocstring(node: ast.AST) -> str:
    """
    提取节点的docstring。

    :param node: AST节点
    :type node: ast.AST
    :return: 节点的docstring，如果没有则返回空字符串
    :rtype: str
    """

    if (node.body and isinstance(node.body[0], ast.Expr) and
        isinstance(node.body[0].value, ast.Constant) and
        isinstance(node.body[0].value.value, str)):
        return node.body[0].value.value
    return ""

def formatDocstring(docstring: str, indent_level: int = 0) -> str:
    """
    格式化docstring为多行格式。

    :param docstring: 要格式化的docstring文本
    :type docstring: str
    :param indent_level: 缩进级别，0表示无缩进，1表示4空格缩进，依此类推
    :type indent_level: int
    :return: 格式化后的多行docstring
    :rtype: str
    """

    if not docstring:
        return ""

    indent = " " * (indent_level * 4)
    lines = docstring.strip().splitlines()
    result = [f'{indent}"""']
    result.extend(f"{indent}{line}" for line in lines)
    result.append(f'{indent}"""')
    return "\n".join(result)

def formatArg(arg: ast.arg) -> str:
    """
    格式化参数（含注解）。

    :param arg: AST参数节点
    :type arg: ast.arg
    :return: 格式化后的参数字符串
    :rtype: str
    """

    text = arg.arg
    if arg.annotation is not None:
        try:
            text += f": {ast.unparse(arg.annotation)}"
        except Exception:
            pass
    return text

def formatArgs(args_node: ast.arguments) -> str:
    """
    格式化参数列表，正确处理 `/` 与 `*` 分隔符。

    :param args_node: 参数节点
    :type args_node: ast.arguments
    :return: 参数列表字符串
    :rtype: str
    """

    parts = []
    if args_node.posonlyargs:
        parts.extend(formatArg(arg) for arg in args_node.posonlyargs)
        parts.append("/")
    parts.extend(formatArg(arg) for arg in args_node.args)
    if args_node.vararg:
        parts.append(f"*{args_node.vararg.arg}")
    if args_node.kwonlyargs:
        if args_node.vararg is None:
            parts.append("*")
        parts.extend(formatArg(arg) for arg in args_node.kwonlyargs)
    if args_node.kwarg:
        parts.append(f"**{args_node.kwarg.arg}")
    return ", ".join(parts)

def formatSignature(node: ast.FunctionDef | ast.AsyncFunctionDef, *, indent_level: int) -> list[str]:
    """
    生成函数或方法的存根行（装饰器 + 签名 + docstring 或 `...`）。

    :param node: 函数节点
    :type node: ast.FunctionDef | ast.AsyncFunctionDef
    :param indent_level: 缩进级别
    :type indent_level: int
    :return: 存根行列表
    :rtype: list[str]
    """

    lines = []
    indent = " " * (indent_level * 4)
    for decorator in node.decorator_list:
        try:
            name = ast.unparse(decorator)
        except Exception:
            continue
        base = name.split(".")[-1].split("(")[0]
        if base in _KEEP_DECORATORS:
            lines.append(f"{indent}@{name}")
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    signature = f"{prefix} {node.name}({formatArgs(node.args)})"
    if node.returns is not None:
        try:
            signature += f" -> {ast.unparse(node.returns)}"
        except Exception:
            pass
    lines.append(f"{indent}{signature}:")
    docstring = getDocstring(node)
    if docstring:
        lines.append(formatDocstring(docstring, indent_level + 1))
    else:
        lines.append(f"{indent}    ...")
    return lines

def formatClass(node: ast.ClassDef) -> list[str]:
    """
    生成类的存根行（基类 + docstring + 属性 + 方法）。

    :param node: 类节点
    :type node: ast.ClassDef
    :return: 存根行列表
    :rtype: list[str]
    """

    lines = []
    bases = []
    for base in node.bases:
        try:
            bases.append(ast.unparse(base))
        except Exception:
            bases.append("Any")
    class_def = f"class {node.name}"
    if bases:
        class_def += f"({', '.join(bases)})"
    class_def += ":"
    lines.append(class_def)

    docstring = getDocstring(node)
    if docstring:
        lines.append(formatDocstring(docstring, 1))
        lines.append("")

    has_content = False
    for item in node.body:
        if isinstance(item, ast.AnnAssign):
            try:
                target = ast.unparse(item.target)
                annotation = ast.unparse(item.annotation)
                if item.value is not None:
                    lines.append(f"    {target}: {annotation} = {ast.unparse(item.value)}")
                else:
                    lines.append(f"    {target}: {annotation}")
                has_content = True
            except Exception:
                pass
        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    try:
                        lines.append(f"    {target.id} = {ast.unparse(item.value)}")
                    except Exception:
                        lines.append(f"    {target.id} = ...")
                    has_content = True
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if item.name.startswith("_") and not (item.name.startswith("__") and item.name.endswith("__")):
                continue
            lines.extend(formatSignature(item, indent_level = 1))
            has_content = True

    if not has_content:
        lines.append("    ...")
    return lines

def generatePyi(source: str) -> str:
    """
    生成.pyi文件的内容。

    :param source: Python源代码字符串
    :type source: str
    :return: 生成的.pyi文件内容
    :rtype: str
    """

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return f'"""类型存根文件解析错误: {e}"""\n'

    blocks = []
    docstring = getDocstring(tree)
    blocks.append(formatDocstring(docstring, 0) if docstring else '"""存根文件"""')

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            try:
                blocks.append(ast.unparse(node))
            except Exception:
                pass
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            try:
                annotation = ast.unparse(node.annotation)
                if node.value is not None:
                    blocks.append(f"{node.target.id}: {annotation} = {ast.unparse(node.value)}")
                else:
                    blocks.append(f"{node.target.id}: {annotation}")
            except Exception:
                pass
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        blocks.append(f"{target.id} = {ast.unparse(node.value)}")
                    except Exception:
                        blocks.append(f"{target.id} = ...")
        elif isinstance(node, ast.ClassDef):
            blocks.append("\n".join(formatClass(node)))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            blocks.append("\n".join(formatSignature(node, indent_level = 0)))

    return "\n\n".join(blocks) + "\n"

def generatePyiByFile(source: pathlib.Path | str, target: pathlib.Path | str, *, encoding: str = "utf-8") -> None:
    """
    通过文件生成.pyi。

    :param source: 源文件
    :type source: pathlib.Path | str
    :param target: 目标文件
    :type target: pathlib.Path | str
    :param encoding: 文件编码
    :type encoding: str
    """

    source = pathlib.Path(source)
    target = pathlib.Path(target)
    target.write_text(generatePyi(source.read_text(encoding = encoding)), encoding = encoding)

def generatePyiByDir(source: pathlib.Path | str, target: pathlib.Path | str, *, encoding: str = "utf-8", copy_existed_pyi = True) -> None:
    """
    通过目录生成.pyi。

    :param source: 源目录
    :type source: pathlib.Path | str
    :param target: 目标目录
    :type target: pathlib.Path | str
    :param encoding: 文件编码
    :type encoding: str
    :param copy_existed_pyi: 是否复制已存在的.pyi文件
    :type copy_existed_pyi: bool
    """

    source = pathlib.Path(source)
    target = pathlib.Path(target)
    target.mkdir(parents = True, exist_ok = True)
    if copy_existed_pyi:
        pyis = source.rglob("*.pyi")
        for i in pyis:
            try:
                rel_path = i.relative_to(source)
                output_path = target / rel_path.with_suffix('.pyi')
                output_path.parent.mkdir(parents = True, exist_ok = True)
                shutil.copy(i, output_path)
            except Exception as error:
                traceback.print_exception(error)
    pys = source.rglob("*.py")
    for i in pys:
        try:
            rel_path = i.relative_to(source)
            output_path = target / rel_path.with_suffix('.pyi')
            output_path.parent.mkdir(parents = True, exist_ok = True)
            generatePyiByFile(i, output_path)
        except Exception as error:
            traceback.print_exception(error)
