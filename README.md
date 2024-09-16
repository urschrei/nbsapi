# NBS API

## Installation
`pip install nbsapi`

## Development
Ensure that you have [`uv`](https://docs.astral.sh/uv/) installed.

1. Clone the repo
2. Inside the repo, create a new virtual env, `.venv`
3. Activate it
4. Run `uv sync` to install packages
5. Run tests using `pytest .`
6. You can now run the FastAPI server using `uvicorn nbsapi.api:app --reload`
7. The API is available on `http://127.0.0.1:8000` and docs at `http://127.0.0.1:8000/docs`

## Database
We're using SQLAlchemy and [alembic](https://alembic.sqlalchemy.org/en/latest/). To run a migration:

1. Make changes to models under `src/nbsapi/models/` (don't forget to import them in `src/nbsapi/models/__init__.py`)
2. Generate a revision using uv run alembic revision --autogenerate -m "description of change"
3. Inspect the generated revision in `src/alembic/versions`
4. When you're happy, apply it: `uv run alembic upgrade head` (you should also run this after you pull changes)
