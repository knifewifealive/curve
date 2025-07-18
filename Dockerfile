FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pytest requests

COPY autotests /autotests
COPY . .


CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & python /autotests/wait_for_api.py && pytest /autotests/api/users_test.py"]