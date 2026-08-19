import pathlib
import os
import shutil
import argparse

base_dir = pathlib.Path(__file__).parent.resolve()
source_dir = pathlib.Path("E:/HHD/bootstrap/static/bootstrap-icons").resolve()
target_dir = base_dir / "HDpip/assets/icon/bootstrap-icons"

def copy(bi_name: str) -> None:
    """
    复制指定名称的 Bootstrap Icons SVG 文件到目标目录。

    :param bi_name: Bootstrap Icons 名称（不含扩展名）
    :type bi_name: str
    """

    source_file = source_dir / f"{bi_name}.svg"
    target_file = target_dir / f"{bi_name}.svg"

    if not source_file.is_file():
        print(f"源文件不存在: {source_file}")
        return

    os.makedirs(target_dir, exist_ok = True)
    shutil.copy(source_file, target_file)
    print(f"已复制: {source_file} -> {target_file}")

def delete(bi_name: str) -> None:
    """
    删除目标目录中的指定名称的 Bootstrap Icons SVG 文件。

    :param bi_name: Bootstrap Icons 名称（不含扩展名）
    :type bi_name: str
    """

    target_file = target_dir / f"{bi_name}.svg"

    if not target_file.is_file():
        print(f"目标文件不存在: {target_file}")
        return

    os.remove(target_file)
    print(f"已删除: {target_file}")

def search(bi_name: str) -> None:
    """
    搜索指定名称的 Bootstrap Icons SVG 文件并打开搜索网页。

    :param bi_name: Bootstrap Icons 名称（不含扩展名）
    :type bi_name: str
    """

    os.system(f"start https://icons.bootstrap.ac.cn/?q={bi_name}")

def main() -> None:
    actions = {
        "copy": copy,
        "delete": delete,
        "search": search,
    }

    parser = argparse.ArgumentParser(description = "Bootstrap Icons 文件管理工具")
    subparsers = parser.add_subparsers(dest = "action", required = True)

    for name, func in actions.items():
        subparser = subparsers.add_parser(
            name,
            description = func.__doc__.strip().splitlines()[0].strip(),
            help = func.__doc__.strip().splitlines()[0].strip(),
        )
        subparser.add_argument("bi_name", help = "Bootstrap Icons 名称（不含扩展名）")

    args = parser.parse_args()

    actions[args.action](args.bi_name)

if __name__ == "__main__":
    main()