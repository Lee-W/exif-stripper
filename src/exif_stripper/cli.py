"""Tool for stripping image metadata (EXIF)."""

from __future__ import annotations

import argparse
from typing import Sequence

from PIL import Image, UnidentifiedImageError

from . import __version__


def process_image(filename: str) -> bool:
    """
    Process image metadata.

    Parameters
    ----------
    filename : str
        The image file to check.

    Returns
    -------
    bool
        Indicator of whether metadata was stripped.
    """
    try:
        with Image.open(filename) as im:
            exif = im.getexif()
            if exif:
                exif.clear()
                im.save(filename)
                return True
    except (FileNotFoundError, UnidentifiedImageError):
        pass
    return False


def main(argv: Sequence[str] | None = None) -> int:
    """
    Tool for stripping EXIF data from images.

    Parameters
    ----------
    argv : Sequence[str] | None, optional
        The arguments passed on the command line.

    Returns
    -------
    int
        Exit code for the process: if metadata was stripped,
        this will be 1 to stop a commit as a pre-commit hook.
    """
    parser = argparse.ArgumentParser(prog='strip-exif')
    parser.add_argument(
        'filenames',
        nargs='*',
        help='Filenames to process.',
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    args = parser.parse_args(argv)

    results = [process_image(filename) for filename in args.filenames]
    return min(1, sum(results))


if __name__ == '__main__':
    raise SystemExit(main())
