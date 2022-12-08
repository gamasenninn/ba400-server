FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install jsonc_parser
COPY ./app /app