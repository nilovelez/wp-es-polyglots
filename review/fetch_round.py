#!/usr/bin/env python3
"""Download a review round from translate.wordpress.org (no login needed).

Usage:
  python3 review/fetch_round.py <project url> [round folder]

<project url> is a GlotPress translation set URL, e.g.
  https://translate.wordpress.org/projects/wp-plugins/<slug>/stable-readme/es/default/
or the project URL without the locale part (es/default is added).

Writes into the round folder (default: review/rounds/NN-<slug>-<subproject>/):
  original.po   waiting strings (the ones to review)
  current.po    approved strings of the same project (for consistency)
"""
import os
import re
import sys
import urllib.parse
import urllib.request

LOCALE = 'es/default'
HERE = os.path.dirname(os.path.abspath(__file__))


def export_url(base, status):
    q = urllib.parse.urlencode({'filters[status]': status, 'format': 'po'})
    return f'{base}export-translations/?{q}'


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    url = sys.argv[1].split('?')[0].rstrip('/') + '/'
    m = re.match(r'https://translate\.wordpress\.org/projects/(.+?)/$', url)
    if not m:
        sys.exit('Not a translate.wordpress.org project URL')
    path = m.group(1)
    if not re.search(r'/[a-z]{2,3}(?:-[a-z]+)?/default$', path):
        path = f'{path}/{LOCALE}'
    base = f'https://translate.wordpress.org/projects/{path}/'
    parts = path.split('/')[:-2]  # drop locale and slug
    name = '-'.join(parts[1:]) if parts[0] in ('wp-plugins', 'wp-themes') else '-'.join(parts)

    if len(sys.argv) > 2:
        folder = sys.argv[2]
    else:
        rounds = os.path.join(HERE, 'rounds')
        nums = [int(d[:2]) for d in os.listdir(rounds) if d[:2].isdigit()]
        folder = os.path.join(rounds, f'{max(nums, default=0) + 1:02d}-{name}')
    os.makedirs(folder, exist_ok=True)

    for status, fname in (('waiting', 'original.po'), ('current', 'current.po')):
        req = urllib.request.Request(export_url(base, status), headers={'User-Agent': 'wp-es-polyglots review tool'})
        data = urllib.request.urlopen(req, timeout=60).read()
        open(os.path.join(folder, fname), 'wb').write(data)
        count = data.decode('utf-8', 'replace').count('\nmsgid ') - 1
        print(f'{fname}: {count} {status} strings')
    print(folder)


if __name__ == '__main__':
    main()
