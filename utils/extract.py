# extract.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

base_url = 'https://fashion-studio.dicoding.dev/'

def extract_product_data(product):
    try:
        title = product.select_one('.product-title').text.strip() if product.select_one('.product-title') else ''
        price_text = product.select_one('.price-container').text.strip() if product.select_one('.price-container') else '0'

        # Extract angka dari price_text (contoh: "Rp 120.000" atau "$7.5")
        price_match = re.findall(r"[\d\.]+", price_text)
        price = float(price_match[0]) if price_match else 0

        details = product.find_all('p')

        # Rating (contoh: "⭐ 4.7 / 5.0") -> ambil 4.7
        rating_text = details[0].text if len(details) > 0 else '0'
        rating_match = re.findall(r"[\d\.]+", rating_text)
        rating = float(rating_match[0]) if rating_match else 0

        # Colors (contoh: "2 Colors")
        colors_text = details[1].text if len(details) > 1 else '0'
        colors_match = re.findall(r"\d+", colors_text)
        colors = int(colors_match[0]) if colors_match else 0

        # Size (contoh: "Size: M")
        size = details[2].text.replace('Size:', '').strip().upper() if len(details) > 2 else 'N/A'

        # Gender (contoh: "Gender: Male")
        gender = details[3].text.replace('Gender:', '').strip().lower() if len(details) > 3 else 'unisex'

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            'name': title,
            'price': price,
            'rating': rating,
            'color': colors,
            'size': size,
            'gender': gender,
            'timestamp': timestamp
        }

    except Exception as e:
        print(f"[Extract Error] {e}")
        return None

def scrape_all_pages():
    all_data = []
    print("Mulai ekstraksi semua halaman...")

    for page in range(1, 51):
        url = f"{base_url}page{page}" if page > 1 else base_url
        print(f"Mengambil halaman {page}...")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Halaman {page} gagal: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.select('.collection-card')

            if not products:
                print(f"Tidak ada produk di halaman {page}")
                continue

            for product in products:
                data = extract_product_data(product)
                if data:
                    all_data.append(data)

            time.sleep(1)

        except Exception as e:
            print(f"[Scraping Error] Halaman {page}: {e}")
            continue

    print(f"Total produk yang berhasil diekstrak: {len(all_data)}")
    return all_data
