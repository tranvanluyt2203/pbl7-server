import requests

token = ""


def register(URL):
    url = URL + "/api/v1/register"
    # data = {"email": "tranvanluyt12b4@gmail.com", "password": "22032002"}
    data = {"email": "tranvanluyt11b4@gmail.com", "password": "22032002"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    print(response.status_code)
    print(response.json())


def login(URL):
    url = URL + "/api/v1/login"
    print(url)
    # data = {"email": "tranvanluyt12b4@gmail.com", "password": "22032002"}
    data = {"email": "tranvanluyt11b4@gmail.com", "password": "12345678"}
    response = requests.post(url, json=data)
    global token
    token = response.json().get("accessToken")
    print("Status code:", response.status_code)
    print("Response:", response.json())


def crawl_data(URL):
    url = URL + "/api/v1/crawl_data?type=3&numPage=1"
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


# ----------------------------

if __name__ == "__main__":
    main()
