from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import os
import google.generativeai as genai
import base64

import requests

# Set up Gemini API Key
genai.configure(api_key=settings.GEMINI_API_KEY)

class CVUploadView(View):
    def get(self, request, *args, **kwargs):
        """Render the upload form."""
        return render(request, 'home.html', {})

    # def post(self, request, *args, **kwargs):
    #     """Handles CV upload and analysis using Gemini AI."""
    #     if 'cv' not in request.FILES:
    #         return JsonResponse({'error': 'No file uploaded'}, status=400)

    #     uploaded_file = request.FILES['cv']
    #     upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
    #     os.makedirs(upload_dir, exist_ok=True)
    #     file_path = os.path.join(upload_dir, uploaded_file.name)

    #     # Save file
    #     with open(file_path, 'wb') as destination:
    #         for chunk in uploaded_file.chunks():
    #             destination.write(chunk)

    #     try:
    #         # Analyze CV with Gemini
    #         analysis = self.analyze_cv_with_gemini(file_path)
    #     except Exception as e:
    #         analysis = f"Error processing CV: {str(e)}"

    #     # ✅ Render results in result.html
    #     return render(request, 'result.html', {'message': "CV processed successfully", 'analysis': analysis})

    def post(self, request):
        if 'cv' not in request.FILES:
            return JsonResponse({"error": "No CV file uploaded"}, status=400)
        
        uploaded_file = request.FILES['cv']
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, uploaded_file.name)

        # Save file
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Gửi file đến API Flask
        api_url = "http://127.0.0.1:5101/receiveCV"
        files = {'cv': open(file_path, 'rb')}
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Failed to process CV"}, status=500)
    # def analyze_cv_with_gemini(self, file_path):
    #     """Uploads the CV PDF file to Gemini and requests analysis."""
    #     model_name = "models/gemini-1.5-pro-002"
    #     model = genai.GenerativeModel(model_name)

    #     # ✅ Upload the PDF file to Gemini
    #     with open(file_path, "rb") as pdf_file:
    #         pdf_content = pdf_file.read()
    #         base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
            
    #     prompt = "Phân tích nội dung của CV này:"

    #     # Tạo phần dữ liệu đa phương tiện cho file PDF
    #     pdf_data = {
    #         "mime_type": "application/pdf",
    #         "data": base64_pdf
    #     }

    #     # Gửi yêu cầu đến Gemini API
    #     response = model.generate_content(
    #         [prompt, pdf_data],
    #         stream=False
    #     )

    #     # Trả về nội dung phản hồi
    #     return response.text