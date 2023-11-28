
docker build -f  ./Dockerfile -t yourtube-api-prod:latest . 

docker run --name yta  -p 8000:80 -it --env-file .env/.env.main yourtube-api-prod:latest