#!/usr/bin/env python3
"""Chèn/cập nhật `const EXTRA = {...};` (English + ngữ pháp) vào index.html, ngay sau dòng `const DATA = ...;`.
Dùng: python3 tools/build_extra.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from extra_data import EN, GRAM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'index.html')


def main():
  lines = open(PATH, encoding='utf-8').read().split('\n')
  di = next(i for i, l in enumerate(lines) if l.startswith('const DATA = '))
  data = json.loads(lines[di][len('const DATA = '):].rstrip(';'))

  zhs, toks = [], set()
  for sec in data['sections']:
      for it in sec['items']:
          zhs.append(''.join(t.get('zh') or t['p'] for t in it['t']))
          toks.update(t['zh'] for t in it['t'] if 'zh' in t)
  missing_en = sorted(toks - set(EN)); missing_gr = [z for z in zhs if z not in GRAM]
  assert not missing_en, 'thiếu English: %s' % missing_en
  assert not missing_gr, 'thiếu ngữ pháp: %s' % missing_gr
  extra = {'en': {k: v for k, v in EN.items() if k in toks}, 'gram': {z: GRAM[z] for z in zhs}}
  new = 'const EXTRA = ' + json.dumps(extra, ensure_ascii=False) + ';'
  if lines[di + 1].startswith('const EXTRA = '): lines[di + 1] = new
  else: lines.insert(di + 1, new)
  open(PATH, 'w', encoding='utf-8').write('\n'.join(lines))
  print('OK: %d câu, %d từ' % (len(zhs), len(toks)))


if __name__ == '__main__':
    main()
