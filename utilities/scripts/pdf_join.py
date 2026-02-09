#!/usr/local/bin/python

import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit(1)
    all_pdf_files = []
    for pdf_file in [Path(argument) for argument in sys.argv[1:]]:
        preamble_pdf_file = pdf_file.parent / f'_{pdf_file.name}'
        os.system(f'echo {pdf_file.name} | enscript -B -q -p - --media=A4 | ps2pdf -sPAPERSIZE=a4 -r300 - {preamble_pdf_file}')
        all_pdf_files.append(str(preamble_pdf_file))
        all_pdf_files.append(str(pdf_file))
    all_arguments = ' '.join(all_pdf_files)
    os.system(f'pdfunite {all_arguments} _.pdf')
