import requests


def register():
    url = "http://127.0.0.1:5000/register"
    data = {"email": "tranvanluyt12b4@gmail.com", "password": "22032002"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    print(response.status_code)
    print(response.json())


def login():
    url = "http://127.0.0.1:5000/login"
    data = {"email": "tranvanluyt12b4@gmail.com", "password": "22032002"}
    response = requests.post(url, json=data)

    print("Status code:", response.status_code)
    print("Response:", response.json())


def main():
    select = -1
    while select != 0:
        print("1. Register")
        print("2. Login")
        print("0. To out")
        print("")
        select = int(input("Type your select : "))
        if select == 1:
            register()
        elif select == 2:
                login()
            


# ----------------------------

if __name__ == "__main__":
    main()
