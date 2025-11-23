#!/bin/bash
source .env
uvicorn cody_agent.api.main:app --reload --port 8000
