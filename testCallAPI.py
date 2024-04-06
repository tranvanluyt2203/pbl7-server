import requests

token = ""


def register():
    url = "http://127.0.0.1:5000/api/v1/register"
    data = {"email": "tranvanluyt12b4@gmail.com", "password": "22032002"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    print(response.status_code)
    print(response.json())


def login():
    url = "http://127.0.0.1:5000/api/v1/login"
    data = {"email": "tranvanluyt12b4@gmail.com", "password": "22032002"}
    response = requests.post(url, json=data)
    global token
    token = response.json().get("accessToken")
    print("Status code:", response.status_code)
    print("Response:", response.json())


def crawl_data():
    url = "http://127.0.0.1:5000/api/v1/crawl_data?type=3&numPage=1"
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response:", response.json())


def push_local_to_firebase():
    url = "http://127.0.0.1:5000/api/v1/push_local_to_firebase"
    response = requests.post(url)
    print("Status code", response.status_code)
    print("Response:", response.json())


def getDetailProductById():
    url = "http://127.0.0.1:5000/api/v1/get_detail_product_by_id"
    productId = input("Enter Product Id : ")
    params = {"productId": productId}
    response = requests.get(url, params=params)
    print("Status code", response.status_code)
    print("Response:", response.json())


def getProductByName():
    url = "http://127.0.0.1:5000/api/v1/search_product_by_name"
    find = input("Enter text to find : ")
    params = {"find": find}
    response = requests.get(url, params=params)
    print("Status code", response.status_code)
    print("Response:", response.json())


def logout():
    url = "http://127.0.0.1:5000/api/v1/logout"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    response = requests.post(url, headers=headers)
    print("Status code", response.status_code)
    print("Response:", response.json())


def add_to_cart():
    url = "http://127.0.0.1:5000/api/v1/add_to_cart"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    idProduct = input("Enter IdProduct : ")
    params = {"idProduct": idProduct}
    response = requests.post(url, headers=headers, params=params)
    print("Status code", response.status_code)
    print("Response:", response.json())


def get_cart():
    url = "http://127.0.0.1:5000/api/v1/get_cart"
    global token
    headers = {"Authorization": f"Bearer{token}"}
    response = requests.get(url, headers=headers)
    print("Status code", response.status_code)
    print("Response:", response.json())


def main():
    select = -1
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
        print("0. To out")
        print("")
        select = int(input("Type your select : "))
        if select == 1:
            register()
        elif select == 2:
            login()
        elif select == 3:
            crawl_data()
        elif select == 4:
            push_local_to_firebase()
        elif select == 5:
            getDetailProductById()
        elif select == 6:
            getProductByName()
        elif select == 7:
            add_to_cart()
        elif select == 8:
            get_cart()
        elif select == 9:
            logout()


# ----------------------------

if __name__ == "__main__":
    main()
