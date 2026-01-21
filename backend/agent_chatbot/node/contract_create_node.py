from agent_chatbot.agent_state.agent_state import ContractState
import os
import httpx
import json
import re
from docxtpl import DocxTemplate
import docx2txt
from docx import Document
import jinja2
from vietnam_number import n2w


LLM_API_URL = os.getenv("LLM_API_URL")
MODEL_NAME = "qwen2.5:7b"

async def analysis_value_input_node(state: ContractState):
    """
        Là một node trong hệ thống agent tạo hợp đồng
        - Dùng llm để lọc thông tin từ input người dùng
    """


    print("="*100+"\n")
    print("- Node analysis")
    print("\n"+"="*100)

    # print(f"- History: {state.get('history_data_input')}")
    # print(f"- Template input: {state.get('data_input')}")

    # Gọi qua cho qwen2.5-32B để trích dữ liệu
    if(state.get("data_history_input")!=None):
        current_data_str = json.dumps(state.get("data_history_input"), ensure_ascii=False)
    else:
        current_data_str = "Không có dữ liệu cũ"

    # print(current_data_str)
    # print(state.get("data_history_input"))
    print(state)
    data_history_input = await extract_information_to_json(state.get("user_input"), state.get("target_schema"), current_data_str)
    print(data_history_input)
    if isinstance(data_history_input, str):
        cleaned_data = data_history_input.strip()
        if cleaned_data.startswith("```"):
            cleaned_data = re.sub(r"^```[a-zA-Z]*\s*", "", cleaned_data)
            cleaned_data = re.sub(r"\s*```$", "", cleaned_data)
        
        cleaned_data = cleaned_data.strip() 
    
        data_history_input = json.loads(cleaned_data)

    # print(data_history_input)
    data_history_input = data_history_input 
    

    # check null cho đầu ra của chatbot
    data_input_null = get_missing_fields(data_history_input)
    # print(f"- Input vừa thu thập được: {data_history_input}")
    # print(f"- Các trường còn thiếu: {data_input_null}")
    # print(f"- Chatbot response: {data_history_input}")


    # Qua bot cuối hỏi lại hoặc check lại (còn null thì hỏi, hết null thì xuất ra cho user check.) 
    # print(state)

    if(len(data_input_null)!=0):
        return {
            "data_history_input":data_history_input,
            "data_input_null":data_input_null,
            "status":"pending"
        }
    else:
        return {
            "data_history_input":data_history_input,
            "data_input_null":["Không có dữ liệu cũ"],
            "status":"pending"
        }


def ask_or_create_node(state: ContractState):
    print("="*100+"\n")
    print("- Node chọn tạo hay hỏi lại")
    print("\n"+"="*100)

    print(state.get("data_input_null"))

    if(state.get("data_input_null")[0]!="Không có dữ liệu cũ"):
        print("- Hỏi lại vì còn null")
        return "ask_value_input_node"
    else:
        print("- Tạo word")
        return "create_word"
    
    

async def ask_value_input_node(state: ContractState):
    """
        Là một node trong hệ thống agent tạo hợp đồng
        - Dùng llm để  hỏi lại người dùng hoặc xuất ra hết cho người dùng kiếm tra
    """


    print("="*100+"\n")
    print("- Node hỏi lại người dùng")
    print("\n"+"="*100)
    # lấy ra các trường thiếu thông tin 
    data_input_null = state.get('data_input_null')
    
    
    # payload
    payload = {
    "model": "qwen2.5:7b",
    "messages": [
            {
                "role": "system", 
                "content": (
                    "Bạn là trợ lý soạn thảo hợp đồng chuyên nghiệp.\n"
                    "Nhiệm vụ: Soạn lời nhắn yêu cầu người dùng bổ sung các thông tin còn thiếu.\n"
                    "- Liệt kê chính xác tên các biến kỹ thuật (key) bị thiếu.\n"
                    "- Với mỗi biến, hãy giải thích ý nghĩa của nó bằng tiếng Việt một cách khách quan và dễ  hiểu.\n"
                    "- Giọng văn: nghiêm túc.\n"
                )
            },
            {
                "role": "user", 
                "content": f"Danh sách các trường thông tin cần thu thập: {data_input_null}"
            }
        ],
        "temperature": 0.7, # Tăng nhẹ lên để câu từ tự nhiên hơn, 0 sẽ bị hơi máy móc
        # "response_format": {"type": "json_object"}  <-- XÓA DÒNG NÀY
    }

    timeout = httpx.Timeout(1200.0, connect=5.0)
    content = ""
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(LLM_API_URL, json=payload)
            raw_text = response.text.strip()
            if isinstance(raw_text, str):
                data = json.loads(raw_text)
            else:
                data = raw_text
            content = data['choices'][0]['message']['content']
        except httpx.HTTPStatusError as e:
            print(f"Lỗi HTTP: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Lỗi không xác định khi gọi vLLM: {e}")
    # print(state)
    return {
        "status":"pending",
        "mess": content,
    }


def create_word(state: ContractState):
    """
        Là một node trong hệ thống agent tạo hợp đồng
            - Dùng code để  parse input vào word 
    """

    print("="*100+"\n")
    print("- Node tạo word cho người dùng")
    print("\n"+"="*100)
    doc = DocxTemplate("database/dot/template/"+state.get("template_id"))
    jinja_env = jinja2.Environment()
    jinja_env.filters['currency'] = currency_filter
    jinja_env.filters['to_vietnamese_words'] = to_vietnamese_words
    doc.render(state.get("data_history_input"), jinja_env)
    doc.save("database/dot/contract/"+state.get("template_id"))
    print("✅ Đã xuất file thành công!")


    return {
        "status":"approve"
    }






def to_vietnamese_words(value):
    if not value: return ""
    number_str = str(int(round(float(value))))
    
    # Gọi hàm n2w với chuỗi số
    result = n2w(number_str)
    
    return str(result.capitalize()).upper()

def currency_filter(value):
    try:
        if value is None:
            return "0"
        return "{:,.0f}".format(float(value)).replace(",", ".")
    except (ValueError, TypeError):
        return value
























async def extract_information_to_json(user_query: str, target_schema: dict, current_data_str:dict):
    """
        Hàm gọi vLLM để bóc tách thông tin dựa trên schema cung cấp.
        - param user_query: Câu chat của người dùng (ví dụ: "Tôi tên Bảo, cty Alpha Tech...")
        - param target_schema: JSON Schema định nghĩa các trường cần lấy.
    """


    payload = {
    "model": "qwen2.5:7b",
    "messages": [
        {
            "role": "system", 
            "content": (
                "Bạn là trợ lý trích xuất và cập nhật dữ liệu hợp đồng. "
                "Nhiệm vụ: Dựa vào 'Dữ liệu cũ' và 'Yêu cầu mới', hãy trả về một đối tượng JSON duy nhất đã được cập nhật hoàn chỉnh.\n"
                "- Nếu thông tin mới trùng với thông tin cũ, hãy ghi đè bằng thông tin mới.\n"
                "- Nếu đã có thông tin cũ thì trả về thông tin tổng hợp từ mới và cũ, ưu tiên thông tin mới nhưng phải bổ xung các trường còn thiếu bằng thông tin cũ.\n"
                "- Nếu người dùng thêm/sửa/xóa sản phẩm trong danh sách, hãy thực hiện tương ứng để trả về danh sách cuối cùng.\n"
                "- Chỉ trả về JSON thuần (flat structure), KHÔNG bao gồm các trường định nghĩa như 'type', 'properties'.\n"
                "- Chỉ trả về  JSON không giải thích gì thêm.\n" 
            )
        },
        {
            "role": "user", 
            "content": (
                f"1. Dữ liệu cũ (đã có): {current_data_str}\n"
                f"2. Yêu cầu mới từ người dùng: '{user_query}'\n"
                # SỬA ĐỔI QUAN TRỌNG Ở DÒNG DƯỚI ĐÂY:
                f"3. Cấu trúc JSON bắt buộc (điền dữ liệu vào mẫu này): {json.dumps(target_schema, ensure_ascii=False)}"
            )
        }
    ],
    "temperature": 0,
    "response_format": {"type": "json_object"} 
    }
    # print(payload)
    # Timeout lớn vì model 32B cần thời gian suy nghĩ cho các bảng dữ liệu dài
    timeout = httpx.Timeout(1200.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(LLM_API_URL, json=payload)
            raw_text = response.text.strip()
            if isinstance(raw_text, str):
                data = json.loads(raw_text)
            else:
                data = raw_text
                
            # Trích xuất câu trả lời của AI
            content = data['choices'][0]['message']['content']
            return content
            
        except httpx.HTTPStatusError as e:
            print(f"Lỗi HTTP: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Lỗi không xác định khi gọi vLLM: {e}")
            return None
        

def get_missing_fields(data, parent_key=''):
    missing = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            
            # Kiểm tra giá trị trống
            if value is None or value == "" or (isinstance(value, (int, float)) and value == 0):
                missing.append(full_key)
            else:
                # Đệ quy nếu là dict hoặc list
                missing.extend(get_missing_fields(value, full_key))
                
    elif isinstance(data, list):
        if not data:
            missing.append(f"{parent_key} (danh sách trống)")
        else:
            for i, item in enumerate(data):
                # Tạo chỉ số dòng ví dụ: items[0], items[1]
                missing.extend(get_missing_fields(item, f"{parent_key}[{i+1}]"))
                
    return missing
    




