#!/usr/bin/env python3
"""合并 official + community 数据，生成统计信息 → docs/data/stats.json"""

import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'docs', 'data')


def load_json(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize_authors(all_libraries: list) -> dict:
    """作者名归一化：trim + 忽略大小写合并，保留首次遇到的写法"""
    canonical_map = {}  # lowercase -> canonical form
    authors = {}

    for lib in all_libraries:
        raw_author = lib.get('author', '')
        if not raw_author:
            continue
        raw = raw_author.strip()
        key = raw.lower()

        if key not in canonical_map:
            canonical_map[key] = raw
            authors[raw] = 0

        canonical = canonical_map[key]
        authors[canonical] = authors.get(canonical, 0) + 1

    # 按数量降序
    return dict(sorted(authors.items(), key=lambda x: -x[1]))


def main():
    official = load_json(DATA_DIR + '/official.json')
    community = load_json(DATA_DIR + '/community.json')

    all_libraries = official + community
    authors = normalize_authors(all_libraries)

    stats = {
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_libraries': len(all_libraries),
        'official_count': len(official),
        'community_count': len(community),
        'authors': {
            'total': len(authors),
            'ranking': authors,
        },
    }

    if not all_libraries:
        print('⚠️ 没有数据文件，生成空统计', file=sys.stderr)

    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = DATA_DIR + '/stats.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

    print(
        f'✅ 统计信息生成成功，总库数: {stats["total_libraries"]}',
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
