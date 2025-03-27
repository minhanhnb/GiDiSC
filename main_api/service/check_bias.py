import json
import os
import base64
import google.generativeai as genai

# Lấy đường dẫn tuyệt đối của thư mục gốc
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SECRET_PATH = os.path.join(BASE_DIR, "secret_key", "gemini_api.json")

# Kiểm tra file API key
if not os.path.exists(SECRET_PATH):
    raise FileNotFoundError(f"API key file not found: {SECRET_PATH}")

# Đọc API key từ JSON
with open(SECRET_PATH, "r") as file:
    api_data = json.load(file)
    API_KEY = api_data.get("api_key")

# Cấu hình Gemini AI với API key
genai.configure(api_key=API_KEY)
MODEL_NAME = "models/gemini-1.5-pro-002"

def encode_pdf(file_path):
    """ Mã hóa file PDF sang base64 """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CV file not found: {file_path}")

    with open(file_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')

def check_bias(file_path):
    """ Kiểm tra bias trong CV bằng Gemini API """
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = "Phân tích nội dung của CV này và kiểm tra bias:"
    
    # Mã hóa file PDF
    base64_pdf = encode_pdf(file_path)

    # Dữ liệu PDF gửi lên API
    pdf_data = {
        "mime_type": "application/pdf",
        "data": base64_pdf
    }

    # Gửi yêu cầu đến Gemini API
    response = model.generate_content([prompt, pdf_data], stream=False)

    return response.text if response else "Error processing response"
