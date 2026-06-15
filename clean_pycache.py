import pathlib
import shutil

root = pathlib.Path(__file__).resolve().parent
count = 0

for pycache in root.rglob("__pycache__"):
    shutil.rmtree(pycache)
    print(f"已删除: {pycache}")
    count += 1

print(f"共清除 {count} 个 __pycache__ 目录")
