from bs4 import BeautifulSoup
import requests
import json
import os

from tqdm import tqdm


def Crawl_from_API_shopee():
    url = "https://shopee14.p.rapidapi.com/shopee/search-shopee-products/"
    querystring = {"token": "DaFPkmkh2Y", "keyword": "apple", "country": "vietnam"}
    headers = {
        "X-RapidAPI-Key": "179e2239femshac00626ad1cf537p15461fjsn728a3c27a4d6",
        "X-RapidAPI-Host": "shopee14.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print(data)
    with open("Data/DataShopee.json", "w") as f:
        json.dump(data["results"], f)


def Crawl_from_API_tiki():
    url = "https://api.tiki.vn/v2/seller/stores/aquaria/products?limit=1&page=2"
    response = requests.get(url)
    print(response.status_code)
    data = response.json()
    print(data)
    with open("Data/DataTiki.json", "w") as f:
        json.dump(data["data"], f)


def Crawl_from_muarenhat(numPage=10, path_file_data="Data/DataMuaReNhat.json"):
    base_url = "https://muarenhat.vn"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = {
        "/dien-may-c100000": "Điện máy",
        "/thoi-trang-c110000": "Thời trang",
        "/the-thao-da-ngoai-c120000": "Thể thao & Dã ngoại",
        "/nha-cua-doi-song-c130000": "Nhà cửa & Đời sống",
        "/me-be-c140000": "Mẹ & Bé",
        "/suc-khoe-lam-dep-c150000": "Sức khỏe & Làm đẹp",
        "/o-to-xe-may-xe-dap-c160000": "Ô tô & Xe máy & Xe đạp",
        "/cong-nghiep-xay-dung-c170000": "Công nghiệp & Xây dựng",
        "/may-nong-nghiep-c180000": "Máy nông nghiệp",
        "/nhac-cu-c190000": "Nhạc cụ",
        "/cham-soc-thu-cung-c200000": "Chăm sóc thú cưng",
        "/thiet-bi-y-te-c210000": "Thiết bị y tế",
        "/thuc-pham-do-uong-c220000": "Thực phẩm & Đồ uống",
        "/voucher-dich-vu-c230000": "Voucher & Dịch vụ",
    }
    num_page_categories = 40
    print("Read data")
    k = 0
    num_page = numPage
    data_ = []
    with tqdm(total=(len(categories) * num_page)) as pbar:

        for url in categories.keys():
            for i in range(1, num_page + 1):
                k += 1
                read_url = base_url + url + f"?page={i}&size={num_page_categories}"
                response_ = requests.get(read_url)
                soup_ = BeautifulSoup(response_.text, "html.parser")
                data = []
                products = soup_.find_all("a", {"class": "css-product-card-root"})
                for item in products:
                    link_product = base_url + item["href"] + "/chuyen-huong"
                    images = item.find_all("img")
                    image_product = images[0]["src"]
                    image_logo_brand = images[1]["src"]
                    link_sale = item.find_all("span", {"class": "css-brand-label"})[
                        0
                    ].text
                    rate = item.find_all("meta", {"itemprop": "ratingValue"})
                    rate = rate[0]["content"] if len(rate) else ""
                    name_product = item.find_all(
                        "div", {"class": "css-product-card-title"}
                    )[0].text
                    discount = item.find_all("span", {"class": "css-discount"})
                    discount = discount[0].text if len(discount) else "0%"
                    price_original = item.find_all(
                        "span", {"class": "css-product-card-discount"}
                    )
                    price_original = (
                        price_original[0].text if len(price_original) else "0"
                    )
                    price = item.find_all("span", {"class": "css-product-card-price"})[
                        0
                    ].text
                    data.append(
                        {
                            "name": name_product,
                            "link_product": link_product,
                            "image_product": image_product,
                            "image_logo": image_logo_brand,
                            "link_sale": link_sale,
                            "rate": rate,
                            "discount": discount,
                            "price_original": price_original,
                            "price": price,
                            "category": categories[url],
                        }
                    )
                data_.extend(data)
                pbar.update(1)
    with open(path_file_data, "w") as f:
        json.dump(data_, f, indent=4)
    categories = [
        category.text
        for category in soup.find_all("span", {"class": "css-a8dskn efli4av3"})
    ]


def main():
    # Crawl_from_API_shopee()
    # Crawl_from_API_tiki()
    Crawl_from_muarenhat(20, "Data/DataMuaReNhat.json")


if __name__ == "__main__":
    main()
