#!/usr/local/bin/python

import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    pdf_file = Path(sys.argv[1])
    original_pdf_file = pdf_file.parent / f'{pdf_file.stem}.original{pdf_file.suffix}'
    optimized_pdf_file = pdf_file.parent / f'{pdf_file.stem}.optimized{pdf_file.suffix}'
    pdf_file.rename(original_pdf_file)
    os.system(f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dDownsampleColorImages=true -dDownsampleGrayImages=true -dDownsampleMonoImages=true -dColorImageResolution=150 -dGrayImageResolution=150 -dMonoImageResolution=150 -dGrayImageDownsampleType=/Bicubic -dMonoImageDownsampleType=/Bicubic -dColorImageDownsampleType=/Bicubic -dCompressPages=true -dNOPAUSE -dQUIET -dBATCH -sOutputFile={optimized_pdf_file} {original_pdf_file}')
    original_size = original_pdf_file.stat().st_size
    optimized_size = optimized_pdf_file.stat().st_size
    if optimized_size < original_size:
        optimized_pdf_file.rename(pdf_file)
    else:
        original_pdf_file.rename(pdf_file)
