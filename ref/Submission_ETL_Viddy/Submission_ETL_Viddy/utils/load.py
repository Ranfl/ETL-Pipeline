import os
from dotenv import load_dotenv
import pandas as pd
import logging
import psycopg2
from google.oauth2.service_account import Credentials
import gspread

# Load .env
load_dotenv()

# Konfigurasi DB dari .env
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# save data ke csv
def load_to_csv(df, filename='products.csv'):
    try:
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")

# save data ke postgres
def load_to_postgresql(df, db_config=db_config, table_name="products"):
    conn = None  # Inisialisasi variabel conn sebelum try
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            title TEXT,
            price FLOAT,
            rating FLOAT,
            colors INT,
            size TEXT,
            gender TEXT,
            timestamp TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        for _, row in df.iterrows():
            cursor.execute(
                f"INSERT INTO {table_name} (title, price, rating, colors, size, gender, timestamp) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (row['Title'], row['Price'], row['Rating'], row['Colors'], row['Size'], row['Gender'], row['Timestamp'])
            )
        conn.commit()
        logging.info(f"Data berhasil disimpan ke PostgreSQL ke tabel {table_name}")
    except Exception as e:
        logging.error(f"Terjadi kesalahan saat menyimpan data ke PostgreSQL: {e}")
    finally:
        if conn is not None:
            conn.close()


def load_to_gsheet(df, spreadsheet_id, worksheet_name="ETL Submission", credentials_file='etl-dicoding-459908-f432548ddf6c.json'):
    if df.empty:
        print("Tidak ada data untuk diupload ke Google Sheets.")
        return
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(spreadsheet_id)

        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("Data berhasil diunggah ke Google Sheets.")
    except FileNotFoundError:
        print(f"File kredensial {credentials_file} tidak ditemukan.")
    except gspread.SpreadsheetNotFound:
        print(f"Spreadsheet dengan ID '{spreadsheet_id}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengupload data ke Google Sheets: {e}")
