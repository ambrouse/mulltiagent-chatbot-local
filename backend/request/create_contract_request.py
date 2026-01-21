from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class create_contract_request(BaseModel):
    # Các trường bắt buộc
    user_id: str = Field(..., example="1", description="ID của người dùng")
    session_id: int = Field(..., example=1)
    type_id: str = Field(..., example="hopdongmuaban.docx")
    user_input: str = Field(..., example="Sale: Dạ em chào anh Tuấn ạ. Em là Lan bên công ty cung cấp thiết bị văn phòng. Em gửi anh báo giá cho đợt mua sắm Quý 1 này, anh xem qua giúp em nhé.\nClient: Chào Lan nhé. Anh xem rồi, giá bên em đợt này cũng ổn đấy. Anh chốt lấy mấy món sau để trang bị cho phòng Dev mới nhé.\nĐầu tiên là Laptop MacBook Pro M3, bên em lấy số lượng 5 chiếc. Giá chốt là 45.000.000 đ/chiếc đúng không?\nSale: Dạ đúng rồi anh, 45 triệu một chiếc ạ. Ngoài laptop ra anh có cần thêm màn hình hay phụ kiện gì không ạ?\nClient: Có chứ. Lấy thêm cho anh 10 cái Màn hình Dell UltraSharp nhé. Loại này anh thấy báo giá là 8.500.000 đ/cái.\nMà em ơi, giá này là chưa thuế đúng không? Bên anh xuất hóa đơn lấy VAT bình thường nhé.\nSale: Dạ vâng, giá trên chưa bao gồm thuế ạ. Hiện tại mặt hàng này bên em đang áp dụng mức thuế GTGT là 10% anh nhé. Anh gửi giúp em thông tin pháp nhân để em lên hợp đồng và xuất hóa đơn ạ.\nClient: Ok em. Thông tin bên anh như sau:\nTên công ty là Công ty Cổ phần Công nghệ SoftTech Việt Nam.\nMã số thuế: 0312345678.\nĐịa chỉ đăng ký kinh doanh là: Tầng 12, Tòa nhà Landmark 81, Quận Bình Thạnh, TP.HCM.\nEmail nhận hóa đơn và hợp đồng em gửi về: finance@softtech.vn nhé.\nSale: Dạ em đã note lại thông tin công ty. Về người đại diện ký hợp đồng lần này vẫn là sếp anh hay sao ạ?\nClient: Đúng rồi, người đại diện là ông Trần Minh Tuấn, chức vụ là Tổng Giám Đốc nhé.\nSale: Dạ rõ ạ. Về phần giao hàng, em sẽ giao về địa chỉ trụ sở ở Landmark 81 hay kho khác ạ? Và ai sẽ là người nhận hàng để em báo kho liên hệ ạ?\nClient: À quên, giao hàng thì đừng giao lên văn phòng. Em giao về kho kỹ thuật giúp anh.\nĐịa chỉ kho nhận hàng là: Số 55 Đường số 7, Khu Công nghiệp Tân Bình, TP.HCM.\nNgười nhận hàng là bạn Lê Thị Bích, không phải anh đâu nhé vì anh hay đi vắng.\nEmail của bạn Bích để bên em gửi thông báo giao hàng là: bich.le@softtech.vn.\nSale: Dạ vâng, em xin chốt lại đơn hàng và thông tin giao nhận. Em sẽ gửi bản thảo hợp đồng qua email finance ngay bây giờ ạ. Cảm ơn anh Tuấn nhiều!")


class load_history_contract_request(BaseModel):
    # Các trường bắt buộc
    user_id: str = Field(..., example="1", description="ID của người dùng")
    session_id: int = Field(..., example="1")