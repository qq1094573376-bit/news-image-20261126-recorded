# news-image-20261126 entry point: place entry.png at the output path.
# Pure standard library. No network, no clock, no randomness, so two
# runs land byte for byte the same. Run with no arguments to write the
# default output, or pass a path as the first argument.
from sys import argv
from pathlib import Path as _P
from shutil import copyfile as _copy

_SRC = _P(__file__).resolve().parent / "entry.png"


def _place(target):
    _dest = _P(target)
    _dest.parent.mkdir(parents=True, exist_ok=True)
    _copy(_SRC, _dest)
    print("entry.png ->", target)


_place(argv[1] if len(argv) > 1 else "/output/entry.png")
