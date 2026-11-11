#!/usr/bin/env python3
"""Download a review round from translate.wordpress.org (no login needed).

Usage:
  python3 review/fetch_round.py <project url> [round folder] [--current]

<project url> is a GlotPress translation set URL, e.g.
  https://translate.wordpress.org/projects/wp-plugins/<slug>/stable-readme/es/default/
or the project URL without the locale part (es/default is added).

Writes into the round folder (default: $ROUNDS_DIR/NN-<slug>-<subproject>/; ROUNDS_DIR
defaults to rounds/ in the repository root, ignored by git; rounds are working
material and never go into the repository):
  original.po   waiting strings (the ones to review)
  current.po    only with --current: approved strings of the project. Not used
                by the skill (approved does not mean correct, and large
                projects have thousands); only for occasional analysis.
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
    want_current = '--current' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--current']
    if not args:
        sys.exit(__doc__)
    url = args[0].split('?')[0].rstrip('/') + '/'
    m = re.match(r'https://translate\.wordpress\.org/projects/(.+?)/$', url)
    if not m:
        sys.exit('Not a translate.wordpress.org project URL')
    path = m.group(1)
    if not re.search(r'/[a-z]{2,3}(?:-[a-z]+)?/default$', path):
        path = f'{path}/{LOCALE}'
    base = f'https://translate.wordpress.org/projects/{path}/'
    parts = path.split('/')[:-2]  # drop locale and slug
    name = '-'.join(parts[1:]) if parts[0] in ('wp-plugins', 'wp-themes') else '-'.join(parts)

    if len(args) > 1:
        folder = args[1]
    else:
        rounds = os.environ.get('ROUNDS_DIR', os.path.join(os.path.dirname(HERE), 'rounds'))
        os.makedirs(rounds, exist_ok=True)
        nums = [int(d[:2]) for d in os.listdir(rounds) if d[:2].isdigit()]
        folder = os.path.join(rounds, f'{max(nums, default=0) + 1:02d}-{name}')
    os.makedirs(folder, exist_ok=True)

    exports = [('waiting', 'original.po')] + ([('current', 'current.po')] if want_current else [])
    for status, fname in exports:
        req = urllib.request.Request(export_url(base, status), headers={'User-Agent': 'wp-es-polyglots review tool'})
        data = urllib.request.urlopen(req, timeout=60).read()
        open(os.path.join(folder, fname), 'wb').write(data)
        count = data.decode('utf-8', 'replace').count('\nmsgid ') - 1
        print(f'{fname}: {count} {status} strings')
    print(folder)


if __name__ == '__main__':
    main()
