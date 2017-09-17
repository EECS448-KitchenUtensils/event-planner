#!/bin/bash
# Copyright Zane J Cersovsky 2017
echo "WARNING: This file is deprecated. Use 'make run' instead."
export FLASK_APP=event_planner
export FLASK_DEBUG=True
export PYTHONPATH=$PYTHONPATH:`pwd`/src
flask run -h 0.0.0.0
