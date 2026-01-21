import os
import shutil
import uuid
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import torch

# --- IMPORT MỚI CHO MARKER V1.X ---
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.config.parser import ConfigParser

app = FastAPI(title="Marker PDF Parser (New API)")

# --- GLOBAL VARIABLES ---
converter_cls = None

# --- STARTUP: LOAD MODEL (Chỉ 1 lần) ---
@app.on_event("startup")
async def startup_event():
    global converter_cls
    print("🚀 Đang khởi động... Đang load Models vào GB10...")
    
    # 1. Kiểm tra GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"✅ Device detected: {device}")

    # 2. Tạo config model
    # Load toàn bộ model cần thiết vào VRAM
    try:
        model_dict = create_model_dict()
        
        # 3. Khởi tạo Config Parser
        config_parser = ConfigParser({
            "output_format": "markdown",
            "batch_multiplier": 4, # Tăng tốc cho GB10
            "languages": None      # Auto detect
        })

        # 4. Khởi tạo Converter Class và giữ trong RAM
        # Lưu ý: Marker v1.x dùng class PdfConverter
        converter_cls = PdfConverter(
            config=config_parser.generate_config_dict(),
            artifact_dict=model_dict,
            processor_list=config_parser.get_processors(),
            renderer=config_parser.get_renderer()
        )
        print("✅ Marker V1.x Models đã sẵn sàng phục vụ!")
        
    except Exception as e:
        print(f"❌ Lỗi khi load model: {e}")
        raise e

@app.post("/read-pdf")
def read_pdf(file: Annotated[UploadFile, File()]):
    global converter_cls
    
    if converter_cls is None:
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Model chưa load xong!"})

    request_id = str(uuid.uuid4())
    tmp_filename = f"{request_id}.pdf"
    tmp_path = os.path.join("/tmp", tmp_filename)
    
    try:
        # 1. Lưu file tạm
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Xử lý bằng Converter (New API)
        # Hàm __call__ của PdfConverter nhận đường dẫn file
        rendered = converter_cls(tmp_path)
        
        # 3. Trích xuất text và meta từ kết quả render
        full_text, _, images = text_from_rendered(rendered)
        metadata = rendered.metadata if hasattr(rendered, 'metadata') else {}

        return {
            "status": "success",
            "filename": file.filename,
            "content": full_text,
            "metadata": metadata
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)