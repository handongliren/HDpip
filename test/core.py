import os
import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))
import HDpip

a = HDpip.core.base.Version("0.1.0")
b = HDpip.core.base.Version("1")
c = "2.0"
d = HDpip.core.base.Version("2.0.0")
e = HDpip.core.base.Version("2.0.1")
print(a, b)
print(a >= b)
print(a <= c)
print(c == d)
print(e.multipleCompare("~=2.0,2.0.1"))
print(a.format("2"))
for i in a:
    print(i)
try:
    del(a[0])
except NotImplementedError as e:
    print(f"HDpipError: {e}")

file = "E:\\HDpip-dev\\HDpip\\setting\\auto.zh-CN.json"

d = HDpip.core.base.Data()
d.open(file)
d.load()
print(d["pip"]["mirror"][3]["name"])

print(HDpip.core.base.getBaseDir())
print(HDpip.core.base.getPythonPath())
os.system(f"\"{str(HDpip.core.base.getPythonPath())}\" -m pip --version")
print(HDpip.core.base.getPipVersion())
try:
    print(HDpip.core.base.Version({}))
except TypeError as error:
    print(error)
print(HDpip.core.pip_api.pip_head)
print(HDpip.core.pip_api.version())
print(HDpip.core.pip_api.list_())
print(HDpip.core.pip_api.show("pip"))
print(HDpip.core.base.isDev())
HDpip.core.base.openInExplorer(HDpip.core.pip_api.getPackageDir("pip"))
HDpip.core.base.Version("1.0.0").multipleCompare(">=0.1.0,<2.0.0")
HDpip.core.pip_api.install("a", print, d["pip"]["mirror"][3]["url"])
HDpip.core.pip_api.uninstall("a")
print(HDpip.core.pip_api.compareMirrorSpeed(d["pip"]["mirror"]))

s = HDpip.core.base.Data()
s.open(file)
s.load()
print((s + {"note": "fuck"}).data)
