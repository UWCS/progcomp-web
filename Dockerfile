FROM python:3.10 AS builder

RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN /root/.local/bin/pipenv sync

FROM python:3.10 AS runtime

# copy deps into runtime container
RUN mkdir -pv /app/.venv
COPY --from=builder /app/.venv/ /app/.venv/

# copy in python sources
COPY frontend /app/frontend
COPY backend /app/backend

WORKDIR /app
RUN ls -al
CMD ["./.venv/bin/gunicorn", "--chdir", "/app", "frontend:app",  "-w", "4", "-b", "0.0.0.0:8080"]