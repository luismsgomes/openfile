import os
import os.path
import sys
import pytest
from openfile import openfile


def test_openfile(tmpdir):
    tmpdir = str(tmpdir)
    for ext in ["", ".gz", "bz2", "xz"]:
        fname = os.path.join(tmpdir, "test.txt." + ext)
        with openfile(fname, "wt") as f:
            print("Hello World!", file=f)

        with openfile(fname, "rt") as f:
            for line in f:
                assert line.rstrip("\r\n") == "Hello World!"

    assert openfile("-", "rt") is sys.stdin
    assert openfile("-", "wt") is sys.stdout
    assert openfile("-", "at") is sys.stdout


def test_openfile_makedirs(tmpdir):
    tmpdir = str(tmpdir)
    fname = os.path.join(tmpdir, "a", "b", "c", "test.txt")
    with pytest.raises(FileNotFoundError):
        with openfile(fname, "wt", makedirs=False) as f:
            pass  # with makedirs=False it raises FileNotFoundError
    with openfile(fname, "wt", makedirs=True) as f:
        assert os.path.isfile(fname)  # with makedirs=True it succeeds

    with openfile(fname, "wt", makedirs=True) as f:
        print("Hello World!", file=f)

    with openfile(fname, "rt") as f:
        for line in f:
            assert line.rstrip("\r\n") == "Hello World!"


def test_openfile_expand():
    with pytest.raises(IsADirectoryError):
        with openfile("~/", "rb", expanduser=True) as f:
            pass
    home = os.path.expanduser("~")
    os.environ["HOME"] = home
    if os.getenv("HOME", None) == home:
        with pytest.raises(IsADirectoryError):
            with openfile("${HOME}", "rb", expandvars=True) as f:
                pass
