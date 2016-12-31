import sys

def test_installation():
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 5

class Foo(object):
    pass