#!/bin/bash

# Initialise DB
./.venv/bin/flask --app progcomp db upgrade

# Run Server
./.venv/bin/gunicorn --chdir /app progcomp:app --enable-stdio-inheritance --log-level debug --capture-output --access-logfile - -w 4 -b 0.0.0.0:5000