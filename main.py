from flask import Flask, request, jsonify
import jwt
import datetime
from CrawlData import Crawl_from_API_shopee, Crawl_from_API_tiki, Crawl_from_muarenhat

app = Flask(__name__)

SECRET_KEY = "secret"


# Thực hiện xác thực người dùng
def authenticate(username, password):
    # Đây là nơi bạn thực hiện xác thực người dùng, ví dụ kiểm tra trong cơ sở dữ liệu
    # Trong ví dụ này, chỉ đơn giản là kiểm tra username và password
    if username == "admin" and password == "password":
        return True
    else:
        return False


# Tạo token
def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=30),  # Thời gian hết hạn của token
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# API endpoint để xác thực và tạo token
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if authenticate(username, password):
        token = generate_token(username)
        return jsonify({"token": token.decode("utf-8")})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# API endpoint bảo vệ, chỉ được truy cập nếu có token hợp lệ
@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Protected endpoint", "user": payload["username"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


@app.route("/crawl_data", methods=["GET"])
def crawl_data():
    type_economy = int(request.args.get("type"))
    numPage = int(request.args.get("num_page"))
    print(type(type_economy))
    print(numPage)
    if type_economy == 3:
        print("VAO")
        Crawl_from_muarenhat(numPage, "./Data/TestDataAPI.json")
        return jsonify({"message": "Data crawled successfully", "result": "success"})
    else:
        return jsonify({"error": "Invalid type"}), 400


if __name__ == "__main__":
    app.run(debug=True)
