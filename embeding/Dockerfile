# Dùng Python Slim cho nhẹ (vì Torch mới sẽ tự kèm CUDA runtime)
FROM python:3.11-slim

WORKDIR /app

# 1. Cài git và các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y git build-essential zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Cài đặt PyTorch với CUDA 13.0 (Theo link bạn yêu cầu)
# Lưu ý: --no-cache-dir để giảm dung lượng image
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu130

# 3. 
RUN pip3 install --no-cache-dir fastapi uvicorn FlagEmbedding transformers peft

# 4. Copy code vào sau cùng
COPY main.py .

# Expose port
EXPOSE 8000

# Chạy app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]