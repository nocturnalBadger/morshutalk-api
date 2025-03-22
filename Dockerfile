FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source=https://github.com/nocturnalBadger/morshutalk-api

RUN apt update && apt install -y ffmpeg && apt clean

RUN pip install morshutalk uvicorn[standard] fastapi cryptography
RUN python -c 'import nltk; nltk.download("averaged_perceptron_tagger_eng")'

WORKDIR /opt/morshu
COPY morshuapi.py  /opt/morshu/morshuapi.py

CMD python morshuapi.py

