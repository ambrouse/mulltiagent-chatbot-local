# Base image
FROM python:3.12-slim

# Biến môi trường tối ưu
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TORCH_DEVICE=cuda

# Cài đặt system dependencies cần thiết cho Marker/OpenCV
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Cài đặt Torch theo link bạn yêu cầu (CUDA 13.0)
# Lưu ý: pip sẽ tốn thời gian tải ở bước này
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu130

# 2. Cài đặt Marker và FastAPI
# Cài python-multipart để nhận upload file
RUN pip3 install --no-cache-dir marker-pdf fastapi uvicorn python-multipart

# 3. Copy source code vào
COPY main.py /app/main.py

# 4. Mở port
EXPOSE 8000

# 5. Chạy server với Uvicorn
# Thêm ":app" vào sau chữ "main"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]