#!/usr/bin/env python3
"""抓取 B4X 社区库 (Dropbox HTML 表格) → docs/data/community.json"""

import json
import os
import re
import sys
import urllib.request
import html

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


def extract_cell_text(cell_html: str) -> str:
    """提取 <td> 内的纯文本，将 <img> 替换为 alt 属性"""
    # 替换 img 标签为 alt 文本
    cell_html = re.sub(
        r'<img[^>]*alt=["\']([^"\']*)["\'][^>]*>',
        r'\1',
        cell_html,
        flags=re.IGNORECASE,
    )
    # 去掉所有 HTML 标签
    text = re.sub(r'<[^>]+>', '', cell_html)
    # 解码 HTML 实体
    text = html.unescape(text)
    return text.strip()


B4WHAT_MAP = {
    'b4x': ['B4A', 'B4I', 'B4J', 'B4R'],
    'b4a': ['B4A'],
    'b4i': ['B4I'],
    'b4j': ['B4J'],
    'b4r': ['B4R'],
}


def parse_table(html_text: str) -> list[dict]:
    # 提取所有 <tr> 行
    tr_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.IGNORECASE | re.DOTALL)
    rows = tr_pattern.findall(html_text)

    libraries = []

    # 从第 4 行开始（索引 3），跳过表头
    for tr_content in rows[3:]:
        # 提取所有 <td>
        td_pattern = re.compile(
            r'<td[^>]*>(.*?)</td>', re.IGNORECASE | re.DOTALL
        )
        cells = td_pattern.findall(tr_content)

        if len(cells) < 11:
            continue

        # 提取每个单元格的纯文本
        data = [extract_cell_text(c) for c in cells]

        name = data[3] if len(data) > 3 else ''
        type_val = data[1] if len(data) > 1 else ''

        if not name or not type_val:
            continue

        b4what = data[0].strip().lower() if len(data) > 0 else ''
        tags = B4WHAT_MAP.get(b4what, [])

        version = data[5].strip() if len(data) > 5 else ''
        version = re.sub(r'^[vV]', '', version)

        libraries.append({
            'name': name,
            'desc': data[8] if len(data) > 8 else '',
            'type': type_val,
            'tags': tags,
            'version': version,
            'date': data[6] if len(data) > 6 else '',
            'author': data[4] if len(data) > 4 else '',
            'link': data[9] if len(data) > 9 else '',
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

    output_path = OUTPUT_DIR + '/community.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(libraries, f, ensure_ascii=False)

    print(
        f'✅ 社区库更新成功，共 {len(libraries)} 条',
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
