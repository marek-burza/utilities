#!/usr/bin/env -S uv run --script --quiet

import subprocess
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    password = sys.argv[2]
    pdf_file = Path(sys.argv[1])
    is_open = subprocess.run(
        ['pdfinfo', str(pdf_file)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0
    if is_open:
        original_pdf_file = pdf_file.parent / f'{pdf_file.stem}.original{pdf_file.suffix}'
        pdf_file.rename(original_pdf_file)
        encrypted_pdf_file = pdf_file
        subprocess.run([
            'qpdf', '--encrypt',
            f'--user-password={password}',
            f'--owner-password={password}',
            '--bits=256', '--',
            str(original_pdf_file), str(encrypted_pdf_file),
        ], check=False)
        print(f'🔒 {encrypted_pdf_file}')
    else:
        verified = '✅' if subprocess.run(
            ['qpdf', '--decrypt', f'--password={password}', str(pdf_file), '/dev/null'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode == 0 else '❌'
        print(f'{verified} {pdf_file}')
