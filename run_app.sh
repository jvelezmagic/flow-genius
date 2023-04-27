#!/bin/bash

if [[ "$APP_TYPE" == "streamlit" ]]; then
  poetry run streamlit run streamlit/Home.py
else
  poetry run uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
fi