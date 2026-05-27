#!/usr/bin/env -S uv run --script --quiet

import subprocess
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
        result = subprocess.run(
            ['sha256sum', '-c', str(checksums)],
            capture_output=True, text=True, check=False,
        )
        failures = [line for line in result.stdout.splitlines() if not line.endswith('OK')]
        if failures:
            print('\n'.join(failures))
    else:
        result = subprocess.run(
            ['find', str(path), '-type', 'f', '-exec', 'sha256sum', '{}', '+'],
            capture_output=True, text=True, check=False,
        )
        checksums.write_text(result.stdout)
    # Verify encrypted PDF files
    files = list(path.rglob('*.pdf'))
    for pdf_file in sorted(files):
        is_open = subprocess.run(
            ['pdfinfo', str(pdf_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode == 0
        if is_open:
            print(f'🔓 {pdf_file}')
        else:
            verified = subprocess.run(
                ['qpdf', '--decrypt', f'--password={password}', str(pdf_file), '/dev/null'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode == 0
            print(f'{"✅" if verified else "❌"} {pdf_file}')

