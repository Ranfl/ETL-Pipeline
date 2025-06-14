import pandas as pd
from datetime import datetime
import re

def transform_products(products):
    cleaned = []
    print("Mulai proses transformasi data...")

    for item in products:
        try:
            # Nama Produk
            name = str(item.get("name") or item.get("Title") or "").strip().title()
            if not name or name.lower() in ["", "unknown product"]:
                continue

            # Harga
            price_raw = item.get("price") or item.get("Price") or "0"
            try:
                price_float = float(price_raw)
            except:
                # Ambil angka dari string jika tidak bisa langsung dikonversi
                price_match = re.findall(r"[\d\.]+", str(price_raw))
                price_float = float(price_match[0]) if price_match else 0

            if price_float <= 0:
                continue
            price_idr = int(price_float * 16000)  # konversi ke rupiah

            # Rating
            rating_raw = str(item.get("rating") or item.get("Rating") or "0").strip()
            rating_clean = re.findall(r"[\d\.]+", rating_raw)
            rating = float(rating_clean[0]) if rating_clean else 0
            if rating <= 0 or rating > 5:
                continue

            # Colors
            color_raw = item.get("color") or item.get("Colors") or 0
            if isinstance(color_raw, str):
                color_match = re.findall(r"\d+", color_raw)
                colors = int(color_match[0]) if color_match else 0
            else:
                colors = int(color_raw)
            if colors <= 0:
                continue

            # Size
            size = str(item.get("size") or item.get("Size") or "").strip().upper()
            if not size:
                continue

            # Gender
            gender = str(item.get("gender") or item.get("Gender") or "").strip().lower()
            if not gender:
                continue

            # Timestamp
            timestamp = item.get("Timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Simpan ke list hasil
            cleaned.append({
                "Title": name,
                "Price (Rp)": price_idr,
                "Rating": rating,
                "Colors": colors,
                "Size": size,
                "Gender": gender,
                "Timestamp": timestamp
            })

        except Exception as e:
            print(f"[Transform Error] {e}")
            continue

    df = pd.DataFrame(cleaned).drop_duplicates().dropna()
    print(f"[INFO] Jumlah data setelah transform: {df.shape[0]}")
    return df
