FROM python:3.12 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

WORKDIR /app

# Create and "activate" the virtual environment, and sync deps
# Ensure the installed binary is on the `PATH`
ENV UV_CACHE_DIR=/opt/uv-cache/
ENV PATH="/root/.cargo/bin/:$PATH"
# Use the virtual environment automatically
ENV VIRTUAL_ENV=/app/.venv
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync --locked && uv cache prune --ci

COPY pyproject.toml ./
COPY README.md ./
COPY LICENSE.md ./
COPY src ./src
COPY alembic.ini ./alembic.ini

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .

CMD ["uv", "run", "uvicorn", "nbsapi.main:app", "--host 0.0.0.0", "--port", "8000"]