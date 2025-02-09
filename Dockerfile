FROM python:3.12.3-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN pip install poetry==1.4.2
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY . .

ENTRYPOINT ["python"]
CMD ["__main__.py"]

