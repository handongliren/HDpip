import os
import sys
import json
import urllib.request
import subprocess

TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CODECOV_TOKEN", "")


def run_coverage():
    """运行 pytest 并生成覆盖率报告。"""
    subprocess.run([
        sys.executable, "-m", "pytest", "tests/",
        "--cov", "--cov-report=xml", "--junitxml=junit.xml",
    ], check = True)


def upload_to_codecov(token: str):
    """上传 coverage.xml 到 Codecov。"""
    if not token:
        print("未提供 Codecov token，跳过上传。")
        return

    with open("coverage.xml", "rb") as f:
        data = f.read()

    boundary = "----------codecov_hdpip"
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="package"\r\n\r\n'
        "coverage.xml\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="token"\r\n\r\n'
        f"{token}\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="commit"\r\n\r\n'
        f"{_get_commit_sha()}\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="coverage.xml"\r\n'
        'Content-Type: application/xml\r\n\r\n'
    ).encode() + data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        "https://codecov.io/upload/v2",
        data = body,
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f"上传结果: {result}")
    print(f"查看报告: https://app.codecov.io/github/handongliren/HDpip")


def _get_commit_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text = True, stderr = subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    run_coverage()
    upload_to_codecov(TOKEN)
