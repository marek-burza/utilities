#!/usr/bin/env -S uv run --script --quiet

import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    password = sys.argv[2]
    path = Path(sys.argv[1])
    if not path.is_dir():
        sys.exit(2)
    # Verify checksums
    checksums = Path(f'{path.name}.sha256')
    if checksums.exists():
        os.system(f'sha256sum -c {checksums} | grep -v \'OK$\'')
    else:
        os.system(f'find {path} -type f -exec sha256sum {{}} + > {checksums}')
    # Verify encrypted PDF files
    files = list(path.rglob('*.pdf'))
    for pdf_file in sorted(files):
        open = os.system(f'pdfinfo {pdf_file} > /dev/null 2> /dev/null') == 0
        if open:
            print(f'🔓 {pdf_file}')
        else:
            verified = os.system(f'qpdf --decrypt --password={password} "{pdf_file}" /dev/null > /dev/null 2> /dev/null') == 0
            print(f'{"✅" if verified else "❌"} {pdf_file}')

