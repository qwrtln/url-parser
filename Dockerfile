FROM python:3.12-alpine

RUN adduser -D app

WORKDIR /app

COPY --chown=appuser:app requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app main.py ./

USER app

ENTRYPOINT ["python", "main.py"]
