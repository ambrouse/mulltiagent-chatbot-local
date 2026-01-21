# Multi-Agent Chatbot System

## 1. Kiến trúc Hệ thống

### 1.1. Tác nhân Tạo tài liệu (Document Generation Agent)
* **Trạng thái:** Hoàn thiện (Xong).
* **Mô hình cốt lõi:** `Qwen 2.5 7B`.
* **Phương thức triển khai:** * Chạy trong môi trường Docker Container thông qua **Ollama**.
    * Cung cấp giao diện lập trình ứng dụng (API) tương thích chuẩn OpenAI REST API.
* **Ghi chú kỹ thuật:** Hiện tại hệ thống đang trong quá trình tinh chỉnh Prompt để nâng cao khả năng nội suy các điều lệ phức tạp trong hợp đồng.

### 1.2. Hệ thống Tra cứu RAG (RAG Engine)
* **Trạng thái:** Đang phát triển (In Progress).
* **Mô hình ngôn ngữ (LLM):** `Qwen 2.5 7B` và `Qwen 2.5 33B` (Tùy chọn theo độ phức tạp của truy vấn).
* **Xử lý tài liệu (PDF Parsing):**
    * Sử dụng công cụ **Marker-pdf** để chuyển đổi cấu hình tài liệu sang định dạng máy có thể hiểu được.
    * Môi trường: FastAPI tích hợp GPU (PyTorch 2.5, Python 3.12).
* **Xử lý Vector & Xếp hạng (Embedding & Rerank):**
    * **Embedding Model:** `BGE-M3` (Hỗ trợ đa ngôn ngữ và độ dài ngữ cảnh tốt).
    * **Reranker Model:** `BGE-Reranker-v2-m3` để tối ưu hóa độ chính xác kết quả tìm kiếm.
    * **Triển khai:** Backend riêng biệt bằng FastAPI, cung cấp hai Endpoint tập trung: `/embedding` và `/rerank`.

---

## 2. Danh mục Công nghệ (Tech Stack)

| Thành phần | Công nghệ | Mô tả |
| :--- | :--- | :--- |
| **LLM Engine** | Ollama | Quản lý và thực thi Inference mô hình Qwen. |
| **PDF Processing** | Marker-pdf | Trích xuất văn bản từ PDF chất lượng cao. |
| **Vector Service** | FastAPI + BGE | Xử lý Embedding và Reranking dữ liệu. |
| **Runtime** | Docker | Đảm bảo tính nhất quán của môi trường triển khai. |
| **Hardware** | NVIDIA GPU | Tăng tốc xử lý cho PyTorch và Inference. |