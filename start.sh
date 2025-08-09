#!/bin/bash
# Start Flask backend in the background
gunicorn backend.app:app --bind 0.0.0.0:5000 &

# Start Streamlit frontend (point it to backend URL)
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
