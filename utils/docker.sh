#! /bin/bash

docker build -f  ./Dockerfile -t yourtube-api-prod:latest . 

docker run  -p 8000:8000 -it --env-file .env/.env.dev yourtube-api-prod:latest