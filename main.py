from utils.extract import scrape_all_pages
from utils.transform import transform_products
from utils.load import load_to_csv, load_to_gsheet

def main():
    print("Mulai proses ekstraksi data...")
    raw_data = scrape_all_pages()

    print("\nMulai proses transformasi data...")
    cleaned_df = transform_products(raw_data)

    print("Loading to CSV and Google Sheets...")
    load_to_csv(cleaned_df)

    # Gantilah ID di bawah ini dengan ID Google Spreadsheet kamu
    spreadsheet_id = "1QNirzI3-T5btgxqFSypXwk2kTCHCriY_Ffc9xMkGlOE"
    load_to_gsheet(cleaned_df, spreadsheet_id=spreadsheet_id, worksheet_name="Sheet1")

    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
