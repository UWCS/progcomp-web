FROM python:3.14-bookworm

RUN pip install pipenv

ENV PROJECT_DIR=/app

# Copy project
COPY . ./${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

RUN pipenv install --system --deploy
 
CMD ["gunicorn", "--graceful-timeout", "5", "progcomp:app",  "-w", "4", "-b", "0.0.0.0:5000"]