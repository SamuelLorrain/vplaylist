#!/bin/sh

poetry run uvicorn vplaylist.port.web_api.web_api:app --host 192.168.1.32 --reload &
cd front/ && npx vite dev --host 192.168.1.32 --mode lan &
wait
