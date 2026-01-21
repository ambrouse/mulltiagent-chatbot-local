from fastapi import APIRouter
import httpx
import asyncio
router = APIRouter()

@router.get("/")
def health_check():
    
    return {"status": "ok", "message": "Backend is running"}


@router.get("/test-nemo")
async def health_check():

    url = "http://localhost:8001/v1/chat/completions"
    
    payload = {
        "model": "nvidia/nemotron-3-nano",
        "messages": [
            {"role": "system", "content": "Bạn là chuyên gia trích xuất thực thể (Entity Extraction)."},
            {"role": "user", "content": "Kiểm tra xem câu sau thiếu thông tin gì: 'Tôi tên là Ba, muốn làm hợp đồng cho HTX của mình.'"}
        ],
        "temperature": 0.1
    }

    async with httpx.AsyncClient(timeout=600.0) as client:
        response = await client.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot trả lời: {result['choices'][0]['message']['content']}")
        else:
            print(f"Lỗi: {response.status_code} - {response.text}")
    return {"status": "ok", "message": "Backend is running"}