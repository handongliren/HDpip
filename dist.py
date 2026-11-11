"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

构建分发包脚本。
"""

import pathlib
import shutil
import subprocess
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

base_dir = pathlib.Path(__file__).parent.resolve()


def clean() -> None:
    """
    清理旧的构建产物。
    """

    for name in ["build", "dist", "hdpip.egg-info"]:
        shutil.rmtree(base_dir / name, ignore_errors=True)
        print(f"清理 {base_dir / name}")


def copy() -> None:
    for name in ["README.md", "LICENSE.txt"]:
        if (base_dir / name).is_file():
            shutil.copy2(base_dir / name, base_dir / "HDpip" / name)
            print(f"复制 {base_dir / name} → {base_dir / 'HDpip' / name}")


def requirements() -> None:
    """
    从 pyproject.toml 生成 requirements 文件。

    生成：
        requirements.txt            ← [project].dependencies
        requirements-dev.txt        ← [project.optional-dependencies].dev
        requirements-docs.txt       ← [project.optional-dependencies].docs

    注意：生成的是直接依赖列表，不包含间接依赖的锁定版本。
    需要锁定版本时，改用 pip-compile 或 uv pip compile。
    """

    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    with open(base_dir / "pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    project = pyproject["project"]
    optional = project.get("optional-dependencies", {})

    def write(path: pathlib.Path, deps: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(deps) + "\n", encoding="utf-8")
        print(f"生成 {path.relative_to(base_dir)}")

    write(base_dir / "requirements.txt", project.get("dependencies", []))
    write(base_dir / "requirements-dev.txt", optional.get("dev", []))
    write(base_dir / "requirements-docs.txt", optional.get("docs", []))


def main() -> int:
    """
    清理、复制、生成 requirements，并构建 sdist 与 wheel。

    :return: 运行状态
    :rtype: int
    """

    clean()
    copy()
    requirements()
    completed = subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--wheel", "--no-isolation"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr, file=sys.stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())