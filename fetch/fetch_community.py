#!/usr/bin/env python3
"""抓取 B4X 社区库 (Dropbox HTML 表格) → docs/data/community.json"""

import json
import os
import sys
import urllib.request
from html.parser import HTMLParser

HTML_URL = 'https://www.dropbox.com/s/4punyxbwek8oc8o/b4xgoodies.html?dl=1'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'docs', 'data')


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36'
            ),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    # 尝试 UTF-8，若失败则尝试 ISO-8859-1 转换
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('iso-8859-1')


# 平台 -> 标签映射
B4WHAT_MAP = {
    'b4x': ['B4A', 'B4I', 'B4J', 'B4R'],
    'b4a': ['B4A'],
    'b4i': ['B4I'],
    'b4j': ['B4J'],
    'b4r': ['B4R'],
}


class _TableParser(HTMLParser):
    """用 HTMLParser 解析社区库表格，避免正则解析 HTML 的脆弱性。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._cells: list[str] = []
        self._text = ''
        self._in_td = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == 'tr':
            self._cells = []
            self._in_td = False
            self._text = ''
        elif tag == 'td':
            self._in_td = True
            self._text = ''
        elif tag == 'img' and self._in_td:
            for name, val in attrs:
                if name == 'alt' and val:
                    self._text += val
                    break

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'td':
            self._in_td = False
            self._cells.append(self._text.strip())
        elif tag == 'tr' and self._cells:
            self.rows.append(self._cells)
            self._cells = []

    def handle_data(self, data):
        if self._in_td:
            self._text += data


def parse_table(html_text: str) -> list[dict]:
    parser = _TableParser()
    parser.feed(html_text)

    libraries = []

    # 从第 4 行开始（索引 3），跳过表头
    for cells in parser.rows[3:]:
        if len(cells) < 11:
            continue

        name = cells[3] if len(cells) > 3 else ''
        type_val = cells[1] if len(cells) > 1 else ''

        if not name or not type_val:
            continue

        b4what = cells[0].strip().lower() if len(cells) > 0 else ''
        tags = B4WHAT_MAP.get(b4what, [])

        version = cells[5].strip() if len(cells) > 5 else ''
        if version.startswith('v') or version.startswith('V'):
            version = version[1:]

        libraries.append({
            'name': name,
            'desc': cells[8] if len(cells) > 8 else '',
            'type': type_val,
            'tags': tags,
            'version': version,
            'date': cells[6] if len(cells) > 6 else '',
            'author': cells[4] if len(cells) > 4 else '',
            'link': cells[9] if len(cells) > 9 else '',
        })

    return libraries


def main():
    try:
        html_text = fetch_html(HTML_URL)
    except Exception as e:
        print(f'❌ 抓取社区库HTML失败: {e}', file=sys.stderr)
        sys.exit(1)

    libraries = parse_table(html_text)

    if len(libraries) < 10:
        print(
            f'❌ 社区库数据异常，仅 {len(libraries)} 条',
            file=sys.stderr,
        )
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, 'community.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(libraries, f, ensure_ascii=False)

    print(
        f'✅ 社区库更新成功，共 {len(libraries)} 条',
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
