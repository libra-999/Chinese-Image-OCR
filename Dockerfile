FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
RUN apt update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY package_v1.txt .
# upgrade pip version to avoid error version with package
RUN pip install --upgrade pip && pip install -r package_v1.txt

COPY . .
EXPOSE 7003
CMD [ "uvicorn","main:app", "--host", "0.0.0.0", "--port","7003" ]