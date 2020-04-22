#!/usr/bin/env python3

import hashlib

def checksum(filename, blocksize=65536, as_hex=False):
  hash_fun = hashlib.md5()
  with open(filename, 'rb') as infile:
    for chunk in iter(lambda: infile.read(blocksize), b''):
        hash_fun.update(chunk)
  return hash_fun.hexdigest() if as_hex else hash_fun.digest()
  return hash_fun.hexdigest()
  #return hash_fun.digest()
