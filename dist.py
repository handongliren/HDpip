import os
import shutil

# 清理旧的构建目录
try:
    shutil.rmtree("dist")
    shutil.rmtree("hdpip.egg-info")
except Exception:
    pass

# 运行构建命令
os.system("python -m build --sdist --wheel --no-isolation")
