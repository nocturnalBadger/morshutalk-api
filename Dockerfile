FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source=https://github.com/nocturnalBadger/morshutalk-api

RUN apt update && apt install -y ffmpeg && rm -rf /var/lib/apt/lists/*

RUN pip install morshutalk uvicorn[standard] fastapi cryptography moviepy
RUN python -c 'import nltk; nltk.download("averaged_perceptron_tagger_eng")'

WORKDIR /opt/morshu
COPY morshuapi.py  /opt/morshu/morshuapi.py
COPY assets /opt/morshu/assets

CMD python morshuapi.py

