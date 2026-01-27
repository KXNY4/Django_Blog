FROM python:3.12-slim-bookworm

# Не создавать .pyc файлы, выводить логи сразу
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала копируем только requirements для кэширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем entrypoint и даём права на выполнение
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Копируем остальной код
COPY . .

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
