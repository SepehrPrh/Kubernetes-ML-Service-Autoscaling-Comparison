FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pillow \
    torch \
    torchvision \
    python-multipart

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]