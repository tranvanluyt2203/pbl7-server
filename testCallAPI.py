import requests

token = ""


def register(URL):
    url = URL + "/api/v1/register"
    # data = {"email": "tranvanluyt12b4@gmail.com", "password": "22032002"}
    email = input("Enter email: ")
    password = input("Enter password: ")
    data = {"email": email, "password": password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    print(response.status_code)
    print(response.json())


def login(URL):
    url = URL + "/api/v1/login"
    # data = {"email": "tranvanluyt11b4@gmail.com", "password": "22032002"}
    email = input("Enter email: ")
    password = input("Enter password: ")
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    print("Status code:", response.status_code)
    print("Response:", response.json())
    global token
    if response.status_code != 401:
        token = response.json().get("data").get("accessToken")
    else:
        print(response.json().get("message"))


def crawl_data(URL):
    url = URL + "/api/v1/crawl_data?type=3&numPage=20"
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response:", response.json())


def push_local_to_firebase(URL):
    url = URL + "/api/v1/push_local_to_firebase"
    response = requests.post(url)
    print("Status code", response.status_code)
    print("Response:", response.json())


def getDetailProductById(URL):
    url = URL + "/api/v1/get_detail_product_by_id"
    productId = input("Enter Product Id : ")
    params = {"productId": productId}
    response = requests.get(url, params=params)
    print("Status code", response.status_code)
    print("Response:", response.json())


def getProductByName(URL):
    url = URL + "/api/v1/search_product_by_name"
    find = input("Enter text to find : ")
    params = {"find": find}
    response = requests.get(url, params=params)
    print("Status code", response.status_code)
    print("Response:", response.json())


def logout(URL):
    url = URL + "/api/v1/logout"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    response = requests.post(url, headers=headers)
    print("Status code", response.status_code)
    print("Response:", response.json())


def add_to_cart(URL):
    url = URL + "/api/v1/add_to_cart"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    idProduct = input("Enter IdProduct : ")
    params = {"idProduct": idProduct}
    response = requests.post(url, headers=headers, params=params)
    print("Status code", response.status_code)
    print("Response:", response.json())


def change_password(URL):
    url = URL + "/api/v1/change_password"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    old_password = input("Enter Old Password : ")
    new_password = input("Enter New Password : ")
    re_new_password = input("Re-Enter New Password : ")
    while new_password != re_new_password:
        print("Re-enter Password Don't Match")
        old_password = input("Enter Old Password : ")
        new_password = input("Enter New Password : ")
        re_new_password = input("Re-Enter New Password : ")
    else:
        data = {"old_password": old_password, "new_password": new_password}
        response = requests.post(url, headers=headers, json=data)
        print("Status code", response.status_code)
        print("Response:", response.json())


def get_cart(URL):
    url = URL + "/api/v1/get_cart"
    global token
    print(token)
    headers = {"Authorization": f"Bearer{token}"}
    response = requests.get(url, headers=headers)
    print("Status code", response.status_code)
    print("Response:", response.json())


def get_profile(URL):
    url = URL + "/api/v1/get_profile"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    response = requests.get(url, headers=headers)
    print("Status code", response.status_code)
    print("Response:", response.json())


def update_profile(URL):
    url = URL + "/api/v1/update_profile"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    fullname = input("Nhập họ và tên: ")
    email = input("Nhập email: ")
    phone_num = input("Nhập số điện thoại: ")
    birth_day = input("Nhập ngày/tháng/năm sinh: ")
    data = {
        "fullname": fullname,
        "email": email,
        "phone_number": phone_num,
        "birth_day": birth_day,
        "avatar": "https://ss-images.saostar.vn/wp700/pc/1613810558698/Facebook-Avatar_3.png",
    }
    response = requests.post(url, headers=headers, json=data)
    print("Status code", response.status_code)
    print("Response:", response.json())


def push_data_category(URL):
    url = URL + "/api/v1/push_data_categories"
    response = requests.post(url)
    print("Status code", response.status_code)
    print("Response:", response.json())


def get_categories(URL):
    url = URL + "/api/v1/get_categories"
    response = requests.get(url)
    print("Status code", response.status_code)
    print("Response:", response.json())


def get_list_id_products_from_category(URL):
    url = URL + "/api/v1/get_list_id_products_from_category"
    categories = [
        "Chăm sóc thú cưng",
        "Công nghiệp & Xây dựng",
        "Điện máy",
        "Máy nông nghiệp",
        "Mẹ & Bé",
        "Nhà cửa & Đời sống",
        "Nhạc cụ",
        "Ô tô & Xe máy & Xe đạp",
        "Sức khỏe & Làm đẹp",
        "Thể thao & Dã ngoại",
        "Thiết bị y tế",
        "Thời trang",
        "Thực phẩm & Đồ uống",
        "Voucher & Dịch vụ",
    ]
    print("List categories:")
    for i in range(len(categories)):
        print(f"{i+1} - {categories[i]}")
    choice = int(input("Your choice number: "))
    params = {"name": categories[choice - 1]}
    response = requests.get(url, params=params)
    print("Status code", response.status_code)
    print("Response:", response.json())


import random


def push_data_recommender(URL):
    url = URL + "/api/v1/push_data_recommender"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    data = {
        "product1": random.randint(1, 5),
        "product6": random.randint(1, 5),
        "product5": random.randint(1, 5),
        "product43": random.randint(1, 5),
        "product1": random.randint(1, 5),
        "product4": random.randint(1, 5),
        "product10": random.randint(1, 5),
        "product88": random.randint(1, 5),
    }
    response = requests.post(url, headers=headers, json=data)
    print("Status code", response.status_code)
    print("Response:", response.json())


def product_recommender(URL):
    url = URL + "/api/v1/product_recommender"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    response = requests.get(url, headers=headers)
    print("Status code", response.status_code)
    print("Response:", response.json())


def main():
    select = -1
    url = input("Nhập url ( Để trống nếu url = http://127.0.0.1:5000 ) : ")
    if url == "":
        url = "http://127.0.0.1:5000"
    while select != 0:
        print("1. Register")
        print("2. Login")
        print("3. Crawl data")
        print("4. Push data to firebase")
        print("5. Get Detail Product By Id")
        print("6. Find Product")
        print("7. Add to cart")
        print("8. Get Cart")
        print("9. Logout")
        print("10. Change Password")
        print("11. Get Profile")
        print("12. Update Profile")
        print("13. Push data to category")
        print("14. Get categories")
        print("15. Get list id product from category")
        print("16. Push data recommender")
        print("17. Product recommender")
        print("0. To out")
        print("")
        select = int(input("Type your select : "))
        if select == 1:
            register(url)
        elif select == 2:
            login(url)
        elif select == 3:
            crawl_data(url)
        elif select == 4:
            push_local_to_firebase(url)
        elif select == 5:
            getDetailProductById(url)
        elif select == 6:
            getProductByName(url)
        elif select == 7:
            add_to_cart(url)
        elif select == 8:
            get_cart(url)
        elif select == 9:
            logout(url)
        elif select == 10:
            change_password(url)
        elif select == 11:
            get_profile(url)
        elif select == 12:
            update_profile(url)
        elif select == 13:
            push_data_category(url)
        elif select == 14:
            get_categories(url)
        elif select == 15:
            get_list_id_products_from_category(url)
        elif select == 16:
            push_data_recommender(url)
        elif select == 17:
            product_recommender(url)


# ----------------------------

if __name__ == "__main__":
    main()
