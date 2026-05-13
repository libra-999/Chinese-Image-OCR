FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY package_v1.txt .
# upgrade pip version to avoid error version with package
RUN pip install --upgrade pip && pip install -r package_v1.txt

COPY . .
# generate protobuf file
RUN python -m grpc_tools.protoc -I=./proto/v1 --python_out=. --grpc_python_out=. v1/ocr_image.proto

FROM python:3.10-slim
WORKDIR /app 
COPY --from=builder /app /app/
CMD [ "python","main.py"]