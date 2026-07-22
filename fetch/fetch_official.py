#!/usr/bin/env python3
"""抓取 B4X 官方库 (Google Sheets CSV) → docs/data/official.json"""

import csv
import json
import os
import sys
import urllib.request
import html

CSV_URL = (
    'https://docs.google.com/spreadsheets/d/'
    '1qFvc3Q70RriJS3m_ywBoJvZ47gSTVAuN_X04SI0_XBw/export?format=csv&gid=0'
)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'docs', 'data')


def fetch_csv(url: str) -> str:
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
        return resp.read().decode('utf-8')


def parse_csv(text: str) -> list[dict]:
    reader = csv.reader(text.splitlines())
    libraries = []
    for i, row in enumerate(reader):
        if i == 0:
            continue  # skip header row
        if not row or not row[0].strip():
            continue
        name = row[0].strip() if len(row) > 0 else ''
        if not name or name == 'Library Name':
            continue

        desc = html.unescape(row[1].strip()) if len(row) > 1 else ''
        b4a = row[2].strip() if len(row) > 2 else ''
        b4i = row[3].strip() if len(row) > 3 else ''
        b4j = row[4].strip() if len(row) > 4 else ''
        b4r = row[5].strip() if len(row) > 5 else ''

        tags = []
        if b4a:
            tags.append('B4A')
        if b4i:
            tags.append('B4I')
        if b4j:
            tags.append('B4J')
        if b4r:
            tags.append('B4R')

        libraries.append({
            'name': html.unescape(name),
            'desc': desc,
            'version': row[6].strip() if len(row) > 6 else '',
            'date': row[7].strip() if len(row) > 7 else '',
            'author': row[8].strip() if len(row) > 8 else '',
            'link': row[10].strip() if len(row) > 10 else '',
            'tags': tags,
        })

    return libraries


def main():
    try:
        csv_text = fetch_csv(CSV_URL)
    except Exception as e:
        print(f'❌ 抓取官方库CSV失败: {e}', file=sys.stderr)
        sys.exit(1)

    libraries = parse_csv(csv_text)

    if len(libraries) < 10:
        print(
            f'❌ 官方库数据异常，仅 {len(libraries)} 条',
            file=sys.stderr,
        )
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, 'official.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(libraries, f, ensure_ascii=False)

    print(
        f'✅ 官方库更新成功，共 {len(libraries)} 条',
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
