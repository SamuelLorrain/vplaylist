#!/bin/sh

poetry run uvicorn vplaylist.port.web_api.web_api:app --reload &
cd front/ && npm run dev &
wait
