FROM python:3.9-alpine as base

# Temporary container to install python dependencies with pipenv
FROM base AS python-deps

RUN python3 -m pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


# Final container to run pfbex
FROM base as runtime

RUN adduser --disabled-password pfbex
WORKDIR /home/pfbex
USER pfbex

COPY --from=python-deps /.venv /home/pfbex/.venv

ENV PATH="/home/pfbex/.venv/bin:$PATH"

EXPOSE 8765

ADD . /home/pfbex

ENTRYPOINT ["python3", "-m", "pfbex"]
