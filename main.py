from flask import Flask, request, jsonify, g, redirect, url_for
import jwt
import datetime
from CrawlData import Crawl_from_API_shopee, Crawl_from_API_tiki, Crawl_from_muarenhat
from firebase_admin import credentials, auth, firestore, db
import firebase_admin
from firebase_admin import firestore
import hashlib
import json
from tqdm import tqdm

app = Flask(__name__)

SECRET_KEY = "Bearer"

# Initialize Firebase Admin SDK
cred = credentials.Certificate("./pbl7-fa653-firebase-adminsdk-2mifc-4880062305.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://pbl7-fa653-default-rtdb.asia-southeast1.firebasedatabase.app"
    },
)
db_firestore = firestore.client()

valid_tokens = set()


def hash(content):
    hashed_content = hashlib.sha256(content.encode()).hexdigest()
    return hashed_content


@app.route("/", methods=["GET"])
def home():
    return (
        jsonify(
            {
                "status": "Success",
                "message": "THIS IS HOME API",
            }
        ),
        201,
    )


@app.route("/api/v1/register", methods=["POST"])
def register():
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        user = auth.create_user(email=email, password=password)
        accessToken = "shop" + user.uid + "2203"
        user_data = {
            "email": email,
            "password": hash(password),
            "accessToken": accessToken,
        }
        profile = {
            "fullname": "",
            "email": email,
            "phone_number": "",
            "birth_day": "",
            "avatar": "https://ss-images.saostar.vn/wp700/pc/1613810558698/Facebook-Avatar_3.png",
        }
        db.reference("users").child(user.uid).set(user_data)
        db_firestore.collection("users").document(user.uid).set(user_data)
        db_firestore.collection("profiles").document(user.uid).set(profile)
        return (
            jsonify(
                {
                    "success": True,
                    "status": 201,
                    "message": "User register successfully",
                    "data": {
                        "accessToken": accessToken,
                    },
                }
            ),
            201,
        )
    except firebase_admin.auth.EmailAlreadyExistsError:
        return (
            jsonify(
                {
                    "error": "Email already exists",
                }
            ),
            400,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                }
            ),
            500,
        )


@app.route("/api/v1/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        user = auth.get_user_by_email(email)
        if user:
            ref = db.reference(f"/users/{user.uid}")
            if ref.get()["password"] == hash(password):
                accessToken = ref.get()["accessToken"]
                valid_tokens.add(SECRET_KEY + accessToken)
                return (
                    jsonify(
                        {
                            "success": True,
                            "status": 200,
                            "message": "Login success",
                            "data": {
                                "accessToken": accessToken,
                            },
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify(
                        {
                            "error": "Invalid password",
                        }
                    ),
                    401,
                )
        else:
            return (
                jsonify(
                    {
                        "error": "error",
                    }
                ),
                400,
            )
    except Exception as e:
        return (
            jsonify(
                {"error": str(e)},
            ),
            400,
        )


@app.route("api/v1/get_profile", methods=["GET"])
def get_profile():
    token = request.headers.get("Authorization")
    if token:
        if token in valid_tokens:
            userId = token.split(SECRET_KEY)[1].split("shop")[1].split("2203")[0]
            profile = (
                db_firestore.collection("profiles").document(userId).get().to_dict()
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "status": 200,
                        "message": "Success",
                        "data": {
                            "profile": profile,
                        },
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "Error": "Token is not valid",
                    }
                ),
                401,
            )

    else:
        return (
            jsonify(
                {
                    "Error": "No accessToken",
                }
            ),
            401,
        )


@app.route("api/v1/update_profile", methods=["POST"])
def update_profile():
    token = request.headers.get("Authorization")
    if token:
        if token in valid_tokens:
            userId = token.split(SECRET_KEY)[1].split("shop")[1].split("2203")[0]
            data = request.json
            db_firestore.collection("profiles").document(userId).set(data)

            return (
                jsonify(
                    {
                        "success": True,
                        "status": 200,
                        "message": "Update Your Profile Success",
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "Error": "Token is not valid",
                    }
                ),
                401,
            )

    else:
        return (
            jsonify(
                {
                    "Error": "No accessToken",
                }
            ),
            401,
        )


@app.route("/api/v1/get_detail_product_by_id/", methods=["GET"])
def getDetailProductById():
    productId = request.args.get("productId")
    if productId:
        product_ref = db_firestore.collection("products").document(productId)
        product_data = product_ref.get()
        if product_data.exists:
            return (
                jsonify(
                    {
                        "success": True,
                        "status": 200,
                        "data": {
                            "detailProduct": product_data.to_dict(),
                        },
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "error": "No found product",
                    }
                ),
                404,
            )
    else:
        return (
            jsonify(
                {
                    "error": "The URL is fail",
                }
            ),
            400,
        )


@app.route("/api/v1/search_product_by_name/", methods=["GET"])
def searchProductByName():
    search_query = request.args.get("find")
    if search_query:
        results = []
        products_ref = db_firestore.collection("products")

        query_ref = products_ref.stream()
        for doc in query_ref:
            doc_dict = doc.to_dict()
            if search_query in doc_dict["name"]:
                results.append(doc_dict)

        if results:
            return (
                jsonify(
                    {
                        "success": True,
                        "status": 200,
                        "message": "Search Successfully",
                        "data": {
                            "results": results,
                        },
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "error": "No products found with the given name",
                    }
                ),
                404,
            )
    else:
        return (
            jsonify(
                {
                    "error": "Query parameter 'query' is required",
                }
            ),
            400,
        )


@app.route("/api/v1/change_password", methods=["POST"])
def change_password():
    token = request.headers.get("Authorization")
    if token:
        if token in valid_tokens:
            old_password = request.json.get("old_password")
            new_password = request.json.get("new_password")
            userId = token.split(SECRET_KEY)[1].split("shop")[1].split("2203")[0]
            password = (
                db_firestore.collection("users")
                .document(userId)
                .get()
                .to_dict()
                .get("password")
            )
            if password != hash(old_password):
                return jsonify({"Error": "Incorrect Password"}), 401
            else:
                db.reference("users/" + userId).update({"password": hash(new_password)})
                db_firestore.collection("users").document(userId).update(
                    {"password": hash(new_password)}
                )
                return (
                    jsonify(
                        {
                            "success": True,
                            "status": 200,
                            "message": "Change Password Successfully",
                        }
                    ),
                    200,
                )
        else:
            return (
                jsonify(
                    {
                        "Error": "Token is not valid",
                    }
                ),
                401,
            )

    else:
        return (
            jsonify(
                {
                    "Error": "No accessToken",
                }
            ),
            401,
        )


@app.route("/api/v1/crawl_data", methods=["GET"])
def crawl_data():
    type_economy = int(request.args.get("type"))
    numPage = int(request.args.get("numPage"))
    if type_economy == 3:
        print("Reading Data from Muarenhat")
        Crawl_from_muarenhat(numPage, "./Data/TestData.json")
        return (
            jsonify(
                {
                    "success": True,
                    "status": 200,
                    "message": "Data crawled successfully",
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Invalid type"}), 400


@app.route("/api/v1/push_local_to_firebase", methods=["POST"])
def push_local_to_firebase(path_file_data="Data/TestData.json"):
    data = None
    with open(path_file_data, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return (
                jsonify(
                    {
                        "error": "No data to push ",
                    }
                ),
                400,
            )
    try:
        with tqdm(total=len(data)) as pbar:
            for index, item in enumerate(data):
                # db.reference("products").child(f"product{index + 1}").set(item)
                db_firestore.collection("products").document(f"product{index + 1}").set(
                    item
                )
                pbar.update(1)  # Cập nhật tiến độ

        return (
            jsonify(
                {
                    "success": True,
                    "status": 200,
                    "message": "Push data success",
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {"Error": str(e)},
            ),
            400,
        )


@app.route("/api/v1/add_to_cart", methods=["POST"])
def add_to_card():
    token = request.headers.get("Authorization")
    if token:
        if token in valid_tokens:
            idProduct = request.args.get("idProduct")
            idUser = token.split(SECRET_KEY)[1]
            data = {"idProduct": idProduct}
            db_firestore.collection("cart").document(idUser).set(data)
            return (
                jsonify(
                    {
                        "success": True,
                        "status": 201,
                        "message": "Added to cart",
                    }
                ),
                201,
            )
        else:
            return (
                jsonify(
                    {
                        "Error": "Token is not valid",
                    }
                ),
                401,
            )
    else:
        return (
            jsonify(
                {
                    "Error": "No accessToken",
                }
            ),
            401,
        )


@app.route("/api/v1/get_cart", methods=["GET"])
def get_cart():
    token = request.headers.get("Authorization")
    if token:
        if token in valid_tokens:
            idUser = token.split(SECRET_KEY)[1]
            data = db_firestore.collection("cart").document(idUser).get()
            if data.exists:
                listProduct = data.to_dict()
                return (
                    jsonify(
                        {
                            "success": True,
                            "status": 200,
                            "message": "Danh sách sản phẩm từ giỏ hàng",
                            "data": {
                                "result": listProduct,
                            },
                        }
                    ),
                    200,
                )
            else:
                listProduct = []
                return (
                    jsonify(
                        {
                            "success": True,
                            "status": 200,
                            "message": "Giỏ hàng trống",
                            "data": {
                                "result": listProduct,
                            },
                        }
                    ),
                    200,
                )
        else:
            return (
                jsonify(
                    {
                        "Error": "Token is not valid",
                    }
                ),
                401,
            )
    else:
        return (
            jsonify(
                {
                    "Error": "No accessToken",
                }
            ),
            401,
        )


@app.route("/api/v1/product_recommender", methods=["GET"])
def product_recommender():
    token = request.headers.get("Authorization")
    if token:
        if token in valid_tokens:
            idUser = token.split(SECRET_KEY)[1]
            return (
                jsonify(
                    {
                        "success": True,
                        "status": 201,
                        "message": "List Recommender Product",
                    }
                ),
                201,
            )
        else:
            return (
                jsonify(
                    {
                        "Error": "Token is not valid",
                    }
                ),
                401,
            )
    else:
        return (
            jsonify(
                {
                    "Error": "No accessToken",
                }
            ),
            401,
        )


@app.route("/api/v1/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    if token:
        if token in valid_tokens:
            valid_tokens.remove(token)
            return (
                jsonify(
                    {
                        "success": True,
                        "status": 200,
                        "message": "Logout Success",
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "Error": "Token is not valid",
                    }
                ),
                401,
            )
    else:
        return (
            jsonify(
                {
                    "Error": "No accessToken",
                }
            ),
            401,
        )


if __name__ == "__main__":
    app.run(debug=True)
