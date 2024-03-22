from bs4 import BeautifulSoup
import requests
import json


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


def Crawl_from_muarenhat(numPage=10,path_file_data = "Data/DataMuaReNhat.json"):
    base_url = "https://muarenhat.vn"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    link_categories = [
        link["href"] if link["href"][0] == "/" else "/" + link["href"]
        for link in soup.find_all("a", {"class": "css-y4wghf e1m9qhx20"})
    ]
    link_categories = link_categories[2 : len(link_categories) - 1]
    print(link_categories)
    print(len(link_categories))
    num_page_categories = [250, 40]
    print("Read data")
    k = 0
    num_page = numPage
    for url in link_categories:
        for i in range(1, num_page + 1):
            k += 1
            read_url = base_url + url + f"?page={i}&size={num_page_categories[1]}"
            response_ = requests.get(read_url)
            soup_ = BeautifulSoup(response_.text, "html.parser")
            data = []
            products = soup_.find_all("a", {"class": "css-product-card-root"})
            for item in products:
                link_product = base_url + item["href"] + "/chuyen-huong"
                images = item.find_all("img")
                image_product = images[0]["src"]
                image_logo_brand = images[1]["src"]
                link_sale = item.find_all("span", {"class": "css-brand-label"})[0].text
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
                price_original = price_original[0].text if len(price_original) else "0"
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
                    }
                )
            loading = round(k / (len(link_categories) * num_page) * 100, 2)
            print(f"{loading}%")
            data_ = []
            with open(path_file_data, "r") as f:
                try:
                    data_ = json.load(f)
                except json.JSONDecodeError:
                    data_ = []

            with open(path_file_data, "w") as f:
                data_.append(data)
                json.dump(data_, f, indent=4)
    categories = [
        category.text
        for category in soup.find_all("span", {"class": "css-a8dskn efli4av3"})
    ]


# def main():
#     # Crawl_from_API_shopee()
#     # Crawl_from_API_tiki()
#     Crawl_from_muarenhat()


# if __name__ == "__main__":
#     main()