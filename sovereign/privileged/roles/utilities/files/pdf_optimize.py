#!/usr/bin/python3

import os
import sys
from pathlib import Path


# - screen: 75dpi
# - ebook: 150dpi
# - printer: 300dpi


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    pdf_file = Path(sys.argv[1])
    original_pdf_file = pdf_file.parent / f'{pdf_file.stem}_{pdf_file.suffix}'
    optimized_pdf_file = pdf_file
    pdf_file.rename(original_pdf_file)
    os.system(f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile={optimized_pdf_file} {original_pdf_file}')
