#!/bin/sh

set -e

# - screen: 75dpi
# - ebook: 150dpi
# - printer: 300dpi

mv $1 _$1
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$1 _$1
