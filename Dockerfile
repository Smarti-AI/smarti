# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
RUN apt-get update && apt-get install tesseract-ocr-all -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

RUN black smarti tests
RUN pylint --fail-under=9.9 smarti tests
RUN pytest --cov-fail-under=94 --cov smarti -v tests

ENTRYPOINT ["python3"]
CMD ["./smarti/app.py" ]