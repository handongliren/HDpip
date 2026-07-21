import subprocess
import shutil

# 使用 -m pylint 调用，避免路径问题
cmd = [
    "pylint",
    "--output-format=colorized,text:pylint_report.txt",
    "HDpip/"
]

# 在 PowerShell 中执行，以支持 ANSI 颜色
subprocess.run(cmd, shell = True, executable = shutil.which("powershell.exe"))