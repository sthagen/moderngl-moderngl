import os
import re


def read_file(name):
    f = open(name)
    res = f.read()
    f.close()
    return res


here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.dirname(here)


def test_version():
    setup = read_file(os.path.join(repo, 'setup.py'))
    init = read_file(os.path.join(repo, 'moderngl', '__init__.py'))
    docs = read_file(os.path.join(repo, 'docs', 'conf.py'))

    match0 = re.search(r'version=\'(\d+\.\d+\.\d+)\'', setup, flags=re.M)

    match1 = re.search(r'__version__ = \'(\d+\.\d+\.\d+)\'', init, flags=re.M)
    match2 = re.search(r'version = \'(\d+\.\d+\.\d+)\'', docs, flags=re.M)
    match3 = re.search(r'release = \'(\d+\.\d+\.\d+)\'', docs, flags=re.M)

    assert match0.group(1) == match1.group(1), 'Version error: moderngl/__init__.py'
    assert match0.group(1) == match2.group(1), 'Version error: docs/conf.py'
    assert match0.group(1) == match3.group(1), 'Version error: docs/conf.py'
