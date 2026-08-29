#!/bin/bash
set -e

echo "Waiting for database to initialize..."
sleep 5

echo "Running migrations ..."
alembic upgrade head

echo "Starting Server..."
# For Production
# gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
# For Local Development (gives reload functinality)
python run.py