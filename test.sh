#!/bin/bash
source ~/.bashrc
penv hardback

set -Eexo pipefail

mypy hardback
flake8
pytest
python -m hardback.main test/hardback/data/letters.png test/hardback/data/illuminati.png
open letters.epub
