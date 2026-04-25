FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir fastapi uvicorn pillow
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]