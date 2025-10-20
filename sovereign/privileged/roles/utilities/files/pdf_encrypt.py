#!/usr/bin/python3

import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    password = sys.argv[2]
    pdf_file = Path(sys.argv[1])
    original_pdf_file = pdf_file.parent / f'{pdf_file.stem}_{pdf_file.suffix}'
    encrypted_pdf_file = pdf_file
    pdf_file.rename(original_pdf_file)
    os.system(f'qpdf --encrypt {password} {password} 256 -- {original_pdf_file} {encrypted_pdf_file}')
