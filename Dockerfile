FROM python:3.8-alpine

EXPOSE 8765

RUN adduser --disabled-password pfbex
WORKDIR /home/pfbex/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . /home/pfbex/app
RUN chown pfbex.pfbex . -Rv

USER pfbex

CMD ["python3", "-m", "pfbex"]
