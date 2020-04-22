#!/usr/bin/env python3

import pytest

import duplipach

def test_checksum__small(tmp_path):
  filename = tmp_path / "sample_small.txt"
  with open(filename, 'wt', encoding='utf-8') as outfile:
    outfile.write('Ahoj světe.\n')
  assert duplipach.checksum(filename, as_hex=True) == '43bbb5bc8155e30234d9db729bd1634b'

def test_checksum__medium(tmp_path):
  filename = tmp_path / "sample_medium.txt"
  with open(filename, 'wt', encoding='utf-8') as outfile:
    for i in range(10**4):
      outfile.write('Tak se tak koukám po světě.\n')
  assert duplipach.checksum(filename, as_hex=True) == '550974917d447ff6cac7ff251814502a'

@pytest.mark.skip(reason="There is probably no need to test such large files specifically")
def test_checksum__large(tmp_path):
  filename = "m_sample_large.txt"
  with open(filename, 'wt', encoding='utf-8') as outfile:
    for i in range(3 * 10**7):
      outfile.write('Toto je jen další zcela zbytečný řádek textu.\n')
  assert duplipach.checksum(filename, as_hex=True) == '1bf7313dc1136c7729f08f48c462c96b'
