# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

RUN black smarti tests
RUN pylint --fail-under=9.9 smarti tests
RUN pytest --cov-fail-under=90 -v tests

ENTRYPOINT ["python3"]
CMD ["./smarti/app.py" ]