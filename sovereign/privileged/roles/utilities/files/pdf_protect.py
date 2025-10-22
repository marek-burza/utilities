#!/usr/bin/python3

import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    password = sys.argv[2]
    pdf_file = Path(sys.argv[1])
    original_pdf_file = Path(sys.argv[1])
    encrypted_pdf_file = original_pdf_file.parent / f'{original_pdf_file.stem}_{original_pdf_file.suffix}'
    open = os.system(f'pdfinfo {original_pdf_file} > /dev/null 2> /dev/null') == 0
    if open:
        os.system(f'qpdf --encrypt {password} {password} 256 -- {original_pdf_file} {encrypted_pdf_file}')
        print(f'🔒 {encrypted_pdf_file}')
    else:
        verified = '✅' if os.system(f'qpdf --decrypt --password={password} {original_pdf_file} /dev/null > /dev/null 2> /dev/null') == 0 else '❌'
        print(f'{verified} {original_pdf_file}')
