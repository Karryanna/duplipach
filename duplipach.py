#!/usr/bin/env python3

import filecmp
import hashlib
import queue

from collections import defaultdict
from pathlib import Path

def checksum(filename:str, blocksize:int=65536, as_hex:bool=False):
  hash_fun = hashlib.md5()
  with open(filename, 'rb') as infile:
    for chunk in iter(lambda: infile.read(blocksize), b''):
        hash_fun.update(chunk)
  return hash_fun.hexdigest() if as_hex else hash_fun.digest()

def get_all_files(base_path):
  path_queue = queue.Queue()
  path_queue.put(Path(base_path))
  while not (path_queue.empty()):
    cur_path = path_queue.get()
    if cur_path.is_dir():
      for p in cur_path.iterdir():
        path_queue.put(p)
    elif cur_path.is_file():
      yield cur_path

def check_pair(file1, file2):
  return filecmp.cmp(file1, file2, shallow=False)

def cluster_by_hashes(base_path):
  hashes = defaultdict(set)
  for f in get_all_files(base_path):
    file_hash = checksum(f)
    hashes[file_hash].add(f)
  return hashes

def cluster_keys_as_hex(hashes):
  bin_keys = list(hashes.keys())
  for k in bin_keys:
    hashes[k.hex()] = hashes[k]
    del(hashes[k])

if __name__ == '__main__':
  import argparse

  argparser = argparse.ArgumentParser()
  argparser.add_argument('--list')
  argparser.add_argument('dir')
  argparser.add_argument('--report-all', dest='duplicates_only', action='store_false');
  argparser.add_argument('--duplicates-only', action='store_true')
  args = argparser.parse_args()

  if args.list:
    hashes = cluster_by_hashes(args.dir)
    cluster_keys_as_hex(hashes)
    with open(args.list, 'wt', encoding='utf-8') as outfile:
      for hash, files in sorted(hashes.items()):
        if ((not args.duplicates_only) or (len(files) > 1)):
          outfile.write('{}: {}\n'.format(hash, ', '.join((str(f) for f in files))))
