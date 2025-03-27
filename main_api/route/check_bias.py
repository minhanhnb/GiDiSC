
from flask import Blueprint
import fitz  # PyMuPDF library for PDF processing

from flask import request, jsonify

from service.check_bias import check_bias

cb = Blueprint('check_bias', __name__)
@cb.route("/check_bias", methods=["POST"])
def check_cv_bias():
    if 'cv' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['cv']
    
    # Phân tích PDF
    pdf_text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text("text") + "\n"

    # Kiểm tra bias
    result = check_bias(pdf_text)
    
    return jsonify({"analysis": result})