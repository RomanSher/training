#!/bin/bash
python -m celery -A project worker -l info
