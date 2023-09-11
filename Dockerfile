FROM python:3.10.12

# Сборка зависимостей
ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install --no-cache-dir poetry

COPY .. ./app

WORKDIR /app

COPY poetry.lock pyproject.toml ./
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the app code to the container
COPY .. ./app

CMD ["poetry", "run", "uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]