FROM python:3.9-slim

WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Requirements dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Port'u expose et
EXPOSE 10000

# Çalıştırma komutu
CMD ["python", "TelegramBotu.py"] 