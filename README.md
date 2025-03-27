## The world's first Morshu as a Service (MaaS)!

(unmute video) "Welcome to the GitHub repo for the MorshuTalk API!"



This is a web server wrapper for https://github.com/n0spaces/MorshuTalk, all credit for the actual morshification goes to @n0spaces

Made with [fastapi](https://fastapi.tiangolo.com/) (and it was made fast)

## Usage
https://morshu.yoinks.org/docs#/

Audio:
```
curl -X POST https://morshu.yoinks.org/morsh -H 'Content-Type: application/json' -d '{"message": "hello world"}' -o output.mp3
```

Video:
```
curl -X POST https://morshu.yoinks.org/morsh -H 'Content-Type: application/json' -d '{"message": "well come to the github ree po for the morshu talk ay pee eye", "response_type": "video"}' -o output.mp4
```

## Deploy instructions (don't read this if you're not me)

- Install docker and stuff
- Setup Traefik: https://github.com/nocturnalBadger/traefik-config
- Make sure DNS is setup, update hostname in docker-compose.yml if needed
- Clone this repo, cd
- `docker compose up -d`
