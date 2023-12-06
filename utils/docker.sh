#! /bin/bash

docker build -f  ./Dockerfile -t yourtube-api-main:latest . 

# docker run  -p 8000:8000 -it --env-file .env/.env.dev yourtube-api-prod:latest

sudo docker run  -p 80:8080 -d --env-file .env.main yourtube-api-main:latest
