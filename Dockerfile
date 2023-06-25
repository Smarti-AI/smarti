# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
COPY .env .

RUN black smarti tests
RUN pylint --fail-under=9.5 smarti tests
RUN pytest --cov-fail-under=5 --cov smarti -v tests

ENTRYPOINT ["python3"]
CMD ["./smarti/app.py" ]
