# Python 3.11 tabanlı image
FROM python:3.11-slim

WORKDIR /app

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
