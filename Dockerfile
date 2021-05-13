FROM python:3.8-alpine

EXPOSE 8765

RUN adduser --disabled-password pfbex
WORKDIR /home/pfbex/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER pfbex

ADD . /home/pfbex/app

CMD ["python3", "-m", "pfbex"]
