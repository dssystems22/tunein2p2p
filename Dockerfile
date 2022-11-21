FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./tunein2p2p.py" ]
