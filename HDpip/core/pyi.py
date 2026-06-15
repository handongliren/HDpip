"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于生成.pyi文件。
"""

import traceback
import shutil
import ast
import pathlib

def extractDocstring(node: ast.AST) -> str:
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
    :type indent_level: int, optional
    :return: 格式化后的多行docstring
    :rtype: str
    """

    if not docstring:
        return ""

    indent = " " * (indent_level * 4)
    lines = docstring.strip().split('\n')

    # 如果只有一行，直接返回多行格式
    if len(lines) == 1:
        return f'{indent}"""\n{indent}{lines[0]}\n{indent}"""'

    # 多行docstring
    result = [f'{indent}"""']
    for line in lines:
        result.append(f'{indent}{line}')
    result.append(f'{indent}"""')
    return '\n'.join(result)

def formatArg(arg: ast.arg) -> str:
    """
    格式化参数。

    :param arg: AST参数节点
    :type arg: ast.arg
    :return: 格式化后的参数字符串
    :rtype: str
    """

    try:
        return ast.unparse(arg)
    except:
        return arg.arg if hasattr(arg, 'arg') else str(arg)

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
        print(f"  语法错误: {e}")
        return '"""类型存根文件解析错误"""\n'

    lines = []

    # 提取模块级docstring
    module_docstring = ""
    if (tree.body and isinstance(tree.body[0], ast.Expr) and
        isinstance(tree.body[0].value, ast.Constant) and
        isinstance(tree.body[0].value.value, str)):
        module_docstring = tree.body[0].value.value

    if module_docstring:
        lines.append(formatDocstring(module_docstring, 0))
    else:
        lines.append(formatDocstring(f"存根文件", 0))
    lines.append('')

    # 处理导入
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                lines.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            if node.level > 0:
                module = '.' * node.level + module
            if node.names[0].name == '*':
                lines.append(f"from {module} import *")
            else:
                names = ', '.join(alias.name for alias in node.names)
                lines.append(f"from {module} import {names}")

    # 添加空行（如果有导入）
    if any(line.startswith('import ') or line.startswith('from ') for line in lines[2:]):
        lines.append('')

    # 处理类定义
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_lines = []

            # 类定义
            bases = []
            for base in node.bases:
                try:
                    bases.append(ast.unparse(base))
                except:
                    bases.append("Any")

            class_def = f"class {node.name}"
            if bases:
                class_def += f"({', '.join(bases)})"
            class_def += ":"
            class_lines.append(class_def)

            # 类docstring
            docstring = extractDocstring(node)
            if docstring:
                # 添加docstring，确保后面有空行
                class_lines.append(formatDocstring(docstring, 1))
                class_lines.append('')

            # 类属性
            for item in node.body:
                if isinstance(item, ast.AnnAssign):
                    # 带类型注解的属性
                    try:
                        target = ast.unparse(item.target)
                        annotation = ast.unparse(item.annotation)
                        class_lines.append(f"    {target}: {annotation}")
                    except:
                        pass

                elif isinstance(item, ast.Assign):
                    # 不带类型注解的属性
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            try:
                                value = ast.unparse(item.value)
                                class_lines.append(f"    {target.id} = {value}")
                            except:
                                class_lines.append(f"    {target.id} = ...")

            # 类方法
            methods_added = False
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # 跳过私有方法（但不是特殊方法）
                    if item.name.startswith('_') and not (item.name.startswith('__') and item.name.endswith('__')):
                        continue

                    # 检查装饰器
                    decorators = []
                    for decorator in item.decorator_list:
                        try:
                            decorator_str = ast.unparse(decorator)
                            if decorator_str == "classmethod":
                                decorators.append("@classmethod")
                            elif decorator_str == "staticmethod":
                                decorators.append("@staticmethod")
                            else:
                                decorators.append(f"@{decorator_str}")
                        except:
                            pass

                    # 方法签名
                    try:
                        # 提取方法定义行
                        if isinstance(item, ast.AsyncFunctionDef):
                            def_line = f"async def {item.name}"
                        else:
                            def_line = f"def {item.name}"

                        # 参数
                        args = []
                        for arg in item.args.posonlyargs:
                            args.append(formatArg(arg))
                        for arg in item.args.args:
                            args.append(formatArg(arg))
                        if item.args.vararg:
                            args.append(f"*{formatArg(item.args.vararg)}")
                        for arg in item.args.kwonlyargs:
                            args.append(formatArg(arg))
                        if item.args.kwarg:
                            args.append(f"**{formatArg(item.args.kwarg)}")

                        def_line += f"({', '.join(args)})"

                        # 返回类型
                        if item.returns:
                            returns = ast.unparse(item.returns)
                            def_line += f" -> {returns}"

                        # 提取方法docstring
                        method_docstring = extractDocstring(item)

                        # 添加装饰器和方法
                        for decorator in decorators:
                            class_lines.append(f"    {decorator}")
                        class_lines.append(f"    {def_line}:")
                        if method_docstring:
                            class_lines.append(formatDocstring(method_docstring, 2))
                        else:
                            class_lines.append("        ...")
                        methods_added = True

                    except:
                        pass

            # 如果没有内容，添加省略号
            if len(class_lines) == 1 or (len(class_lines) == 2 and class_lines[1] == ''):
                class_lines.append("    ...")

            lines.extend(class_lines)
            lines.append('')

    # 处理模块级函数
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 检查是否在类中
            in_class = False
            for parent in ast.walk(tree):
                if isinstance(parent, ast.ClassDef) and node in parent.body:
                    in_class = True
                    break

            if not in_class and not node.name.startswith('_'):
                try:
                    # 函数签名
                    if isinstance(node, ast.AsyncFunctionDef):
                        def_line = f"async def {node.name}"
                    else:
                        def_line = f"def {node.name}"

                    # 参数
                    args = []
                    for arg in node.args.posonlyargs:
                        args.append(formatArg(arg))
                    for arg in node.args.args:
                        args.append(formatArg(arg))
                    if node.args.vararg:
                        args.append(f"*{formatArg(node.args.vararg)}")
                    for arg in node.args.kwonlyargs:
                        args.append(formatArg(arg))
                    if node.args.kwarg:
                        args.append(f"**{formatArg(node.args.kwarg)}")

                    def_line += f"({', '.join(args)})"

                    # 返回类型
                    if node.returns:
                        returns = ast.unparse(node.returns)
                        def_line += f" -> {returns}"

                    # 提取函数docstring
                    func_docstring = extractDocstring(node)

                    lines.append(f"{def_line}:")
                    if func_docstring:
                        lines.append(formatDocstring(func_docstring, 1))
                    else:
                        lines.append("    ...")
                    lines.append('')

                except:
                    pass

    return '\n'.join(lines)

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
    :type target: pathlib.Path
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
