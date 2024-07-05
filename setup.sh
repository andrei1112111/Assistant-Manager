#!/bin/sh

python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
echo ""
python ./src/main.py -c