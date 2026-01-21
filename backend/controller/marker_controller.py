# from fastapi import APIRouter, HTTPException, UploadFile, File
# from service.marker_service import marker_predict

# router = APIRouter()

# @router.post("/marker")
# async def marker(file: UploadFile = File(...)):
#     if not file.filename.endswith('.pdf'):
#         raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file PDF")
#     a = await marker_predict(file)

#     return {"status": "ok", "result": a}