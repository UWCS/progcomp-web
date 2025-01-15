FROM python:3.12-bookworm

RUN pip install pipenv

ENV PROJECT_DIR /app

COPY . ./${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}

RUN pipenv install --system --deploy

CMD [ "gunicorn",  ]