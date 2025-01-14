FROM python:3.12 AS builder

RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN ~/.local/bin/pipenv sync

FROM python:3.12 AS runtime

# copy deps into runtime container
RUN mkdir -pv /app/.venv
COPY --from=builder /app/.venv/ /app/.venv/

# copy in python sources
COPY progcomp /app/progcomp

# Add migrations directory to initialise db
COPY migrations /app/migrations

# Add start script
COPY start.sh app/start.sh

WORKDIR /app
RUN chmod +x start.sh

CMD ["./start.sh"]