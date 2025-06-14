import requests
from bs4 import BeautifulSoup
import re
from time import sleep

def extract_products(base_url="https://fashion-studio.dicoding.dev/", pages=50, exchange_rate=16000):
    products = []

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Bot/0.1; +https://example.com/bot)"
    }

    for page in range(1, pages + 1):
        url = f"{base_url}page{page}"
        print(f"Scraping halaman {page} ... URL: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
        except requests.RequestException as e:
            print(f"Request error di halaman {page}: {e}")
            continue

        if response.status_code != 200:
            print(f"Gagal akses halaman {page} dengan status code {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="collection-card")
        print(f"Jumlah produk di halaman {page}: {len(cards)}")

        if not cards:
            print("Tidak ada produk lagi, berhenti.")
            break

        for card in cards:
            name_tag = card.find("h3", class_="product-title")
            price_tag = card.find("span", class_="price")
            details = card.find("div", class_="product-details").find_all("p")

            product_info = {
                "name": "",
                "price": 0.0,
                "rating": 0.0,
                "color": "",
                "size": "",
                "gender": "",
            }

            for detail in details:
                text = detail.text.strip()
                if text.startswith("Rating:"):
                    match = re.search(r"(\d+\.?\d*)", text)
                    product_info["rating"] = float(match.group(1)) if match else 0.0
                elif text.startswith("Size:"):
                    product_info["size"] = text.replace("Size:", "").strip()
                elif text.startswith("Gender:"):
                    product_info["gender"] = text.replace("Gender:", "").strip()
                elif "Color" in text:
                    match = re.search(r"(\d+)", text)
                    if match:
                        product_info["color"] = int(match.group(1))


            if name_tag and price_tag:
                try:
                    price_usd = float(price_tag.text.strip().replace("$", "").replace(",", ""))
                    product_info["price"] = price_usd * exchange_rate
                    product_info["name"] = name_tag.text.strip()
                except ValueError:
                    continue

                # Hanya tambahkan jika kolom wajib terisi
                required_fields = ["name", "price", "rating", "size", "gender"]
                if all(product_info[k] for k in required_fields):
                    products.append(product_info)

        sleep(1)  # hindari beban server

    print(f"\n Total produk yang berhasil diambil: {len(products)}")
    return products
