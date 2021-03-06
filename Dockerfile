FROM python:3.6
WORKDIR /usr/src/app
COPY . .
RUN pip install pipenv && \
    pipenv install --system --deploy
USER 1001
RUN PYTHONPATH=. alembic upgrade head
CMD ["python", "app.py"]
