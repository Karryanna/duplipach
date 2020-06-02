#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path

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

def test_check_pair__same(tmp_path):
  f1 = tmp_path / 'a'
  f2 = tmp_path / 'b'
  txt = 'Ahoj světe'
  with open(f1, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt)
  with open(f2, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt)
  assert duplipach.check_pair(f1, f2) == True

def test_check_pair__different(tmp_path):
  f1 = tmp_path / 'a'
  f2 = tmp_path / 'b'
  txt1 = 'Ahoj světe'
  txt2 = 'Ahoj lidi'
  with open(f1, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt1)
  with open(f2, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt2)
  assert duplipach.check_pair(f1, f2) == False

def test_cluster_by_hashes(tmp_path):
  f1 = tmp_path / 'a'
  f2 = tmp_path / 'b'
  f3 = tmp_path / 'c'
  f4 = tmp_path / 'd'
  txt1 = 'Ahoj světe\n'
  txt2 = 'Čau lidi\n'
  txt3 = 'Páčko\n'

  with open(f1, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt1)
  with open(f2, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt2)
  with open(f3, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt3)
  with open(f4, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt2)

  expected = defaultdict(set)
  expected[b'\x98\xe8\xe2a\x8a3\xceU\xc1S\x98\x90\x91\xe3\xcb9'].add(Path(tmp_path / 'a'))
  expected[b'\xeb\xd3C\x0b^\xbf\xe0_\x13(\x04L\xeb}\xa2\xf8'].add(Path(tmp_path / 'b'))
  expected[b'5\x02\x03\xfd\xa5.\xe5\x9a\xb9F\x1f\x0f\xcc\x86\xe6\xf7'].add(Path(tmp_path / 'c'))
  expected[b'\xeb\xd3C\x0b^\xbf\xe0_\x13(\x04L\xeb}\xa2\xf8'].add(Path(tmp_path / 'd'))

  assert duplipach.cluster_by_hashes(tmp_path) == expected

def test_cluster_keys_as_hex(tmp_path):
  f1 = tmp_path / 'a'
  f2 = tmp_path / 'b'
  f3 = tmp_path / 'c'
  f4 = tmp_path / 'd'
  txt1 = 'Ahoj světe\n'
  txt2 = 'Čau lidi\n'
  txt3 = 'Páčko\n'

  with open(f1, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt1)
  with open(f2, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt2)
  with open(f3, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt3)
  with open(f4, 'wt', encoding='utf-8') as outfile:
    outfile.write(txt2)

  provided = defaultdict(set)
  expected = defaultdict(set)

  provided[b'\x98\xe8\xe2a\x8a3\xceU\xc1S\x98\x90\x91\xe3\xcb9'].add(Path(tmp_path / 'a'))
  provided[b'\xeb\xd3C\x0b^\xbf\xe0_\x13(\x04L\xeb}\xa2\xf8'].add(Path(tmp_path / 'b'))
  provided[b'5\x02\x03\xfd\xa5.\xe5\x9a\xb9F\x1f\x0f\xcc\x86\xe6\xf7'].add(Path(tmp_path / 'c'))
  provided[b'\xeb\xd3C\x0b^\xbf\xe0_\x13(\x04L\xeb}\xa2\xf8'].add(Path(tmp_path / 'd'))

  expected['98e8e2618a33ce55c153989091e3cb39'].add(Path(tmp_path / 'a'))
  expected['ebd3430b5ebfe05f1328044ceb7da2f8'].add(Path(tmp_path / 'b'))
  expected['350203fda52ee59ab9461f0fcc86e6f7'].add(Path(tmp_path / 'c'))
  expected['ebd3430b5ebfe05f1328044ceb7da2f8'].add(Path(tmp_path / 'd'))

  duplipach.cluster_keys_as_hex(provided)
  assert provided == expected
