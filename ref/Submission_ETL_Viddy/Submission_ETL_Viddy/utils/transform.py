import pandas as pd
from datetime import datetime

def transform_products(products):
    cleaned = []
    for item in products:
        try:
            name = item.get("name", "").strip().title()
            price = float(item.get("price", 0))
            rating = float(item.get("rating", 0))
            size = item.get("size", "").upper()
            gender = item.get("gender", "").lower()

            # Tangani berbagai format color
            color_raw = item.get("color", 0)
            if isinstance(color_raw, str):
                colors = int(color_raw.split()[0])
            else:
                colors = int(color_raw)

            if name and price > 0 and rating > 0:
                cleaned.append({
                    "Title": name,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        except Exception as e:
            print(f"Error transforming item: {e}")
            continue

    return pd.DataFrame(cleaned)
