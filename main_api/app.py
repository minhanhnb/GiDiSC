from flask import Flask, jsonify
from flask_cors import CORS

from route.check_bias import cb  # Import CORS

app = Flask(__name__)
CORS(app)
# Đăng ký Blueprint với Flask
app.register_blueprint(cb)

@app.route("/", methods=["GET"])
def home():
    print("Hàm home đã được gọi.")  # In ra màn hình để kiểm tra
    return jsonify({"message": "Ứng dụng Flask đang chạy thành công!"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5101)  # Đảm bảo chạy trên cổng 5000
