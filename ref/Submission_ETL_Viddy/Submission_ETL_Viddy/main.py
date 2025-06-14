from utils.extract import extract_products
from utils.transform import transform_products
from utils.load import load_to_csv, load_to_gsheet

def run_etl():
    print("Extracting data...")
    products = extract_products(pages=50)

    print("Transforming data...")
    df = transform_products(products)

    print("Loading to CSV and Google Sheets...")
    load_to_csv(df)

    # Gantilah ID di bawah ini dengan ID Google Spreadsheet kamu
    spreadsheet_id = "1DKNooPzxGVmgUHeBmwk9El6bEqCbPpcluIiJwnLasdg"
    load_to_gsheet(df, spreadsheet_id=spreadsheet_id, worksheet_name="Sheet1")

    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    run_etl()