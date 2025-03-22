## The world's first Morshu as a Service (MaaS)!


https://morshu.yoinks.org/docs#/

Made with fastapi (and it was made fast)

## Deploy instructions (from scratch on fedora 41)

- install git, docker, certbot
- clone this repo
- `sudo certbot certonly --standalone`
- `docker build -t morshu-api .`
- `docker run -d --restart always -v "/etc/letsencrypt/live/<hostname>/fullchain.pem:/certs/server.crt" -v /etc/letsencrypt/live/<hostname>/privkey.pem:/certs/server.key -e CERTFILE_PATH=/certs/server.crt -e CERT_KEY_PATH=/certs/server.key -p 443:8000 morshu-api`
