#!/usr/bin/python3

import getpass
import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    password = getpass.getpass(prompt='Password: ')
    password_repeated = getpass.getpass(prompt='Password (repeat): ')
    if password == password_repeated:
        pdf_file = Path(sys.argv[1])
        password = f'{pdf_file.stem}{password}'
        original_pdf_file = pdf_file.parent / f'_{pdf_file.name}'
        encrypted_pdf_file = pdf_file
        pdf_file.rename(original_pdf_file)
        os.system(f'qpdf --encrypt {password} {password} 256 -- {original_pdf_file} {encrypted_pdf_file}')
