#!/usr/bin/env -S uv run --script --quiet

import subprocess
import sys
from pathlib import Path


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit(1)
    all_pdf_files = []
    for pdf_file in [Path(argument) for argument in sys.argv[1:]]:
        preamble_pdf_file = pdf_file.parent / f'_{pdf_file.name}'
        enscript_process = subprocess.Popen(
            ['enscript', '-B', '-q', '-p', '-', '--media=A4'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        ps2pdf_process_input, _ = enscript_process.communicate(input=pdf_file.name.encode())
        subprocess.run(
            ['ps2pdf', '-sPAPERSIZE=a4', '-r300', '-', str(preamble_pdf_file)],
            input=ps2pdf_process_input,
            check=False,
        )
        all_pdf_files.append(str(preamble_pdf_file))
        all_pdf_files.append(str(pdf_file))
    subprocess.run(['pdfunite'] + all_pdf_files + ['_.pdf'], check=False)
