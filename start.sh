#!/usr/bin/env bash
set -e

python backend/app.py &

: "${PORT:=8501}"
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
