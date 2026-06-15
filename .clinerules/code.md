# 代码规范

1. 变量文件名小写英文下划线分隔，函数小驼峰命名，类大驼峰命名，str全部双引号，function传参=左右打空格，,后面打空格

2. docstring后空一行写代码，函数间要空行，导入时依次导入基本库、应用库、本体模块，且三类导入之间要空行，本体模块必须相对导入，不写\#注释

3. 使用CRLF行尾序列，使用UTF-8编码

4. 不要自作聪明，有现成轮子不重造，不懂多看我写的，不用质疑我实现的优劣，有错误再指出，能改直接动文件，不能改告诉我

例如:

```python
# test_connect.py

connect_ip = "127.0.0.1"

def connect_init(...) -> None:
    """docstring"""

    # code
    ...

class ConnectPool: ...

print("Hello world!", end = "")
```
