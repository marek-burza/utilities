#!/usr/bin/python3

import getpass
import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    password = getpass.getpass(prompt='Password: ')
    path = Path(sys.argv[1])
    if path.is_dir():
        files = list(path.glob('*.pdf'))
    else:
        files = [path]
    for pdf_file in sorted(files):
        combined_password = f'{pdf_file.stem}{password}'
        open = os.system(f'pdfinfo {pdf_file} > /dev/null 2> /dev/null') == 0
        if open:
            print(f'❌ {pdf_file}')
        else:
            verified = os.system(f'qpdf --decrypt --password={combined_password} {pdf_file} /dev/null > /dev/null 2> /dev/null') == 0
            if verified:
                print(pdf_file)
            else:
                print(f'❌ {pdf_file}')
