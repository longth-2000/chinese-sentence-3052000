#!/usr/bin/env python3
"""Xoá thật các câu đã đánh dấu trong app khỏi index.html.
Dùng: python3 tools/apply_deletes.py deleted.json
(file là JSON copy từ tab "Đã xoá": {"delete": ["一个人。", ...]}; hoặc truyền '-' để đọc stdin)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import build_extra

def main():
    if len(sys.argv) != 2: sys.exit(__doc__)
    raw = sys.stdin.read() if sys.argv[1] == '-' else open(sys.argv[1], encoding='utf-8').read()
    dele = set(json.loads(raw)['delete'])
    path = build_extra.PATH
    lines = open(path, encoding='utf-8').read().split('\n')
    di = next(i for i, l in enumerate(lines) if l.startswith('const DATA = '))
    data = json.loads(lines[di][len('const DATA = '):].rstrip(';'))
    removed = set()
    for sec in data['sections']:
        keep = []
        for it in sec['items']:
            zh = ''.join(t.get('zh') or t['p'] for t in it['t'])
            if zh in dele: removed.add(zh)
            else: keep.append(it)
        sec['items'] = keep
    data['sections'] = [s for s in data['sections'] if s['items']]
    lines[di] = 'const DATA = ' + json.dumps(data, ensure_ascii=False) + ';'
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    print('Đã xoá %d câu; không tìm thấy: %s' % (len(removed), sorted(dele - removed) or 'không'))
    build_extra.main()

main()
