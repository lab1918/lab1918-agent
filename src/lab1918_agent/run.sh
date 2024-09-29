#!/bin/bash

export PYTHONPATH=.

while true; do
    python3 lab1918_agent/rotate.py
    celery -A lab1918_agent.deployer worker --pool=prefork --concurrency=4 --loglevel=info -E
done
