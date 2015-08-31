#!/bin.bash

TIME="$(date +%Y-%m-%d)"
PYTHON="python"


$PYTHON manage.py modelscount 2> $TIME.dat