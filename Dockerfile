FROM python:3.8-alpine

LABEL Name=fbexp Version=0.0.1
EXPOSE 8765

WORKDIR /app
ADD . /app

RUN  python3 -m pip --no-cache-dir install -r requirements.txt

CMD ["python3", "-m", "fbexp"]
