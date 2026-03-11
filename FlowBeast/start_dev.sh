#!/bin/bash
source .env
uvicorn flowbeast.api.main:app --reload --port 8000
