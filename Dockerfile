FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1


WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==$POETRY_VERSION" \
	&& poetry config virtualenvs.create false \
	&& poetry install --only main --no-root

COPY . .

RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

# Запуск
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]