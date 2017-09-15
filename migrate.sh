#!/bin/bash
# Copyright Zane J Cersovsky 2017

export FLASK_APP=event_planner
export FLASK_DEBUG=True
export PYTHONPATH=$PYTHONPATH:`pwd`/src
flask migrate
