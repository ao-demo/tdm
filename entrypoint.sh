#!/bin/bash
set -e

python masker.py >/tmp/dm.log &
python main.py
