# import httpx
# from fastapi import APIRouter, UploadFile, File, HTTPException
# from typing import Any
# import os
# MARKER_URL = os.environ.get("MARKER_URL")

# async def marker_predict(file):
#     file_content = await file.read()
#     files = {
#         "file": (file.filename, file_content, file.content_type)
#     }


#     async with httpx.AsyncClient(timeout=None) as client:
#         response = await client.post(MARKER_URL, files=files)
        
#         # Kiểm tra phản hồi từ Marker
#         if response.status_code != 200:
#             return {
#                 "status": "error",
#                 "marker_error": response.text
#             }
        
#         # 5. Nhận kết quả Markdown
#         data = response.json()
#         markdown_output = data.get("markdown", "")
#         metadata = data.get("metadata", {})

#         # Trả về cho Frontend hoặc xử lý tiếp (ví dụ: băm nhỏ theo #)
#         return {
#             "filename": file.filename,
#             "content": markdown_output,
#             "metadata": metadata,
#             "message": "Xử lý thành công"
#         }