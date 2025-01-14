#!/bin/bash

./.venv/bin/flask --app progcomp db upgrade
./.venv/bin/gunicorn --chdir /app progcomp:app -w 4 -b 0.0.0.0:5000