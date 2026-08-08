"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

GitHub 风格 alerts（> [!NOTE]）的 Python Markdown 扩展，
在渲染前转换为 Material admonition 语法（!!! note "Note"）。
"""

import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

ALERT_RE = re.compile(r"^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
ALERT_MAP = {
    "NOTE": "note",
    "TIP": "tip",
    "IMPORTANT": "warning",
    "WARNING": "warning",
    "CAUTION": "danger",
}
ALERT_TITLES = {
    "NOTE": "Note",
    "TIP": "Tip",
    "IMPORTANT": "Important",
    "WARNING": "Warning",
    "CAUTION": "Danger",
}


class GitHubAlertPreprocessor(Preprocessor):
    """把 `> [!XXX]` 引用块转换为 Material admonition 语法。"""

    def run(self, lines: list[str]) -> list[str]:
        out: list[str] = []
        i = 0
        while i < len(lines):
            m = ALERT_RE.match(lines[i])
            if m:
                key = m.group(1)
                out.append(f'!!! {ALERT_MAP[key]} "{ALERT_TITLES[key]}"')
                i += 1
                while i < len(lines) and lines[i].strip().startswith(">"):
                    out.append("    " + lines[i].strip()[1:].strip())
                    i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1
                out.append("")
            else:
                out.append(lines[i])
                i += 1
        return out


class GitHubAlertExtension(Extension):
    """注册 alerts 转换 preprocessor。"""

    def extendMarkdown(self, md) -> None:
        md.preprocessors.register(GitHubAlertPreprocessor(md), "github_alerts", 30)
