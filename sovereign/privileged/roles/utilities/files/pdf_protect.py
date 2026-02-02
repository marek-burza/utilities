#!/usr/bin/python3

import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    password = sys.argv[2]
    pdf_file = Path(sys.argv[1])
    open = os.system(f'pdfinfo {pdf_file} > /dev/null 2> /dev/null') == 0
    if open:
        original_pdf_file = pdf_file.parent / f'{pdf_file.stem}.original{pdf_file.suffix}'
        pdf_file.rename(original_pdf_file)
        encrypted_pdf_file = pdf_file
        os.system(f'qpdf --encrypt --user-password=\'{password}\' --owner-password=\'{password}\' --bits=256 -- {original_pdf_file} {encrypted_pdf_file}')
        print(f'🔒 {encrypted_pdf_file}')
    else:
        verified = '✅' if os.system(f'qpdf --decrypt --password=\'{password}\' {pdf_file} /dev/null > /dev/null 2> /dev/null') == 0 else '❌'
        print(f'{verified} {pdf_file}')
