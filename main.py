from flask import Flask, request, jsonify
import jwt
import datetime
from CrawlData import Crawl_from_API_shopee, Crawl_from_API_tiki, Crawl_from_muarenhat
from firebase_admin import credentials, auth, firestore, db
import firebase_admin
from firebase_admin import firestore
import hashlib


app = Flask(__name__)

SECRET_KEY = "secret"


# Khởi tạo Firebase Admin SDK
cred = credentials.Certificate("./pbl7-fa653-firebase-adminsdk-2mifc-4880062305.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://pbl7-fa653-default-rtdb.asia-southeast1.firebasedatabase.app"
    },
)


def hash_password(password):
    # Sử dụng thuật toán băm SHA-256 để mã hóa mật khẩu
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


# API endpoint để đăng ký người dùng
@app.route("/register", methods=["POST"])
def register():
    # Nhận thông tin người dùng từ request
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        # Tạo tài khoản người dùng trong Firebase Authentication
        user = auth.create_user(email=email, password=password)
        accessToken = "shop" + user.uid + "2203"
        # Tạo dữ liệu trong Realtime Database
        user_data = {
            "email": email,
            "password": hash_password(password),
            "accessToken": accessToken,
        }
        db.reference("users").child(user.uid).set(user_data)

        return (
            jsonify(
                {
                    "status": "Success",
                    "message": "User registered successfully",
                    "accessToken": accessToken,
                }
            ),
            201,
        )
    except firebase_admin.auth.EmailAlreadyExistsError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    # Nhận dữ liệu đăng nhập từ yêu cầu
    email = request.json.get("email")
    password = request.json.get("password")
    print(password)

    try:
        # Xác thực người dùng với Firebase Authentication
        user = auth.get_user_by_email(email)
        if user:
            ref = db.reference(f"/users/{user.uid}")
            if ref.get()["password"] == hash_password(password):
                accessToken = ref.get()["accessToken"]
                return (
                    jsonify(
                        {
                            "status": "Success",
                            "message": "Login success",
                            "accessToken": accessToken,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"Error": "Invalid password"}), 400

        else:
            return jsonify({"error": "error"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


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
