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
