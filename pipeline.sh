#!/bin/bash
set -e

source .venv/bin/activate

python main.py -dv
python main.py -p
python main.py -a