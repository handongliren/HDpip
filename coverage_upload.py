import os
import sys
import json
import urllib.request
import subprocess


def run_coverage():
    """运行 pytest 并生成覆盖率报告。"""
    import importlib.util

    has_pytest_cov = importlib.util.find_spec("pytest_cov") is not None
    has_coverage = importlib.util.find_spec("coverage") is not None

    if has_pytest_cov:
        subprocess.run([
            sys.executable, "-m", "pytest", "tests/",
            "--cov", "--cov-report=xml", "--junitxml=junit.xml",
        ], check=True)
        return

    if has_coverage:
        subprocess.run([
            sys.executable, "-m", "coverage", "run", "-m", "pytest", "tests/",
        ], check=True)
        subprocess.run([
            sys.executable, "-m", "coverage", "xml", "-o", "coverage.xml",
        ], check=True)
        return

    raise SystemExit(
        "Missing pytest-cov or coverage. Install with `pip install pytest-cov coverage`."
    )


def upload_to_codecov(token: str):
    """上传 coverage.xml 到 Codecov。"""
    if not token:
        print("未提供 Codecov token，跳过上传。")
        return

    # 如果安装了 codecov 包，优先使用其 CLI（更可靠）。
    import importlib.util
    if importlib.util.find_spec("codecov") is not None:
        print("使用已安装的 codecov 包上传 coverage.xml")
        try:
            subprocess.run([
                sys.executable, "-m", "codecov", "-t", token, "-f", "coverage.xml",
            ], check=True)
            print("使用 codecov 包上传成功。")
            return
        except subprocess.CalledProcessError as exc:
            print(f"codecov 包上传失败: {exc}; 回退到 HTTP 上传方式。")

    with open("coverage.xml", "rb") as f:
        data = f.read()

    boundary = "----------codecov_hdpip"

    # Build multipart body parts safely. Include token and commitid only when present.
    parts = []
    parts.append(
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"package\"\r\n\r\n"
        "codecov-python\r\n"
    )

    if token:
        parts.append(
            f"--{boundary}\r\n"
            "Content-Disposition: form-data; name=\"token\"\r\n\r\n"
            f"{token}\r\n"
        )

    # Include a commitid explicitly to satisfy Codecov validation.
    commit = _get_commit_sha()
    if commit:
        commit = commit.strip()
        parts.append(
            f"--{boundary}\r\n"
            "Content-Disposition: form-data; name=\"commitid\"\r\n\r\n"
            f"{commit}\r\n"
        )

    parts.append(
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="coverage.xml"\r\n'
        'Content-Type: application/xml\r\n\r\n'
    )

    body = "".join(parts).encode() + data + f"\r\n--{boundary}--\r\n".encode()

    # Include token in query string as some Codecov endpoints expect it there.
    url = f"https://codecov.io/upload/v4?token={token}"
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )

    # Debug: show first part of body to inspect fields if needed
    try:
        print("--- debug: multipart body head ---")
        print(body[:800].decode(errors="replace"))
        print("--- end debug ---")

        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        print(f"上传结果: {result}")
        print(f"查看报告: https://app.codecov.io/github/handongliren/HDpip")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode(errors="replace")
        raise RuntimeError(
            f"Codecov upload failed: {exc.code} {exc.reason}\n{error_body}"
        ) from exc


def _get_commit_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text = True, stderr = subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    try:
        token = sys.argv[1]
    except IndexError:
        if os.path.exists("codecov.token"):
            with open("codecov.token", encoding = "utf-8") as f:
                token = f.read().strip()
        else:
            token = os.environ.get("CODECOV_TOKEN", "")

    run_coverage()
    upload_to_codecov(token)
