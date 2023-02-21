# elevenbot

## pull
```docker
# pull image from dockerhub
docker pull tylerplesetz/elevenbot:latest
```

## build
```docker
# build image
sudo docker build -t elevenbot .
```


## run
```docker
# create container and run
sudo docker run -d --name elevenbot --env DISCORD_BOT_TOKEN="discord-bot-api-key" --env ELEVENLABS_API="elevenlabs-api-key" tylerplesetz/elevenbot:latest
