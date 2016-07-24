import os.path
from openfile import openfile
import sys


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
