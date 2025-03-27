from django.shortcuts import render

# Create your views here.
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import default_storage
import os

# Khởi tạo Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class UploadCVView(View):
    def post(self, request):
        if "cv_file" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # Lưu file tạm thời
        cv_file = request.FILES["cv_file"]
        file_path = default_storage.save(f"temp/{cv_file.name}", cv_file)

        # Đọc nội dung file (giả sử là PDF hoặc TXT)
        file_content = self.read_file(file_path)

        # Gửi dữ liệu đến Gemini API
        result = self.analyze_cv(file_content)

        # Xóa file sau khi xử lý
        default_storage.delete(file_path)

        return JsonResponse({"result": result})

    def read_file(self, file_path):
        """ Đọc nội dung của file (hiện hỗ trợ TXT, PDF có thể dùng PyMuPDF). """
        _, ext = os.path.splitext(file_path)
        if ext.lower() == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Unsupported file format"

    def analyze_cv(self, cv_text):
        """ Gửi nội dung CV đến Gemini API và nhận kết quả """
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Đánh giá CV sau:\n{cv_text}")
        return response.text
