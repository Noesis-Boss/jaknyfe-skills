#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/workspace/Skills/zobodhi-memory/scripts/memory.ts')

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    save = sub.add_parser('save')
    save.add_argument('--content', required=True)
    save.add_argument('--tags', default='')
    search = sub.add_parser('search')
    search.add_argument('--query', required=True)
    search.add_argument('--limit', default='10')
    sub.add_parser('self-profile')
    args = parser.parse_args()
    if args.command == 'save':
        cmd = ['bun', 'run', str(ROOT), '--add', args.content, '--type=fact', '--project=legacy-supermemory', '--tags=' + args.tags, '--force']
    elif args.command == 'search':
        cmd = ['bun', 'run', str(ROOT), '--query', args.query]
    else:
        cmd = ['bun', 'run', str(ROOT), '--list', '--project=legacy-supermemory']
    raise SystemExit(subprocess.call(cmd, cwd='/home/workspace/Skills/zobodhi-memory'))

if __name__ == '__main__':
    main()
