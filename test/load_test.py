import sys
import os
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_postgresql, load_to_gsheet

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestLoad(unittest.TestCase):

    def test_load_to_csv(self):
        df = pd.DataFrame([{
            "name": "Kaos",
            "price": 50000,
            "rating": 4.5,
            "size": "L",
            "gender": "male"
        }])
        temp_path = "test_output.csv"
        load_to_csv(df, filename=temp_path)
        self.assertTrue(os.path.exists(temp_path))
        os.remove(temp_path)

    @patch('psycopg2.connect')
    def test_load_to_postgresql(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        df = pd.DataFrame([{
            "Title": "Kaos",
            "Price": 50000,
            "Rating": 4.5,
            "Colors": 2,
            "Size": "L",
            "Gender": "male",
            "Timestamp": "2025-05-16 22:00:00"
        }])

        db_config = {
            "host": "localhost",
            "port": 5432,
            "dbname": "testdb",
            "user": "testuser",
            "password": "testpass"
        }

        load_to_postgresql(df, db_config=db_config, table_name="test_products")

        mock_connect.assert_called_once_with(**db_config)
        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)
        self.assertTrue(mock_conn.close.called)

    @patch('psycopg2.connect', side_effect=Exception("DB connection error"))
    def test_load_to_postgresql_exception(self, mock_connect):
        df = pd.DataFrame([{
            "Title": "Kaos",
            "Price": 50000,
            "Rating": 4.5,
            "Colors": 2,
            "Size": "L",
            "Gender": "male",
            "Timestamp": "2025-05-16 22:00:00"
        }])

        # Catch the print output to test if exception is handled gracefully
        with self.assertLogs(level='INFO') as log:
            load_to_postgresql(df)
        # No exception should be raised, just caught and printed

    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_load_to_gsheet(self, mock_creds, mock_authorize):
        mock_creds.return_value = MagicMock()
        mock_client = MagicMock()
        mock_authorize.return_value = mock_client

        mock_spreadsheet = MagicMock()
        mock_client.open_by_key.return_value = mock_spreadsheet

        mock_worksheet = MagicMock()
        mock_spreadsheet.worksheet.side_effect = [mock_worksheet]

        df = pd.DataFrame({
            "Title": ["Kaos"],
            "Price": [50000],
            "Rating": [4.5],
            "Colors": [2],
            "Size": ["L"],
            "Gender": ["male"],
            "Timestamp": ["2025-05-16 22:00:00"]
        })

        load_to_gsheet(df, "fake_spreadsheet_id", worksheet_name="TestSheet")

        mock_client.open_by_key.assert_called_once_with("fake_spreadsheet_id")
        mock_spreadsheet.worksheet.assert_called_once_with("TestSheet")
        mock_worksheet.clear.assert_called_once()
        mock_worksheet.update.assert_called_once()

    def test_load_to_gsheet_empty_df(self):
        df = pd.DataFrame()
        # Should print info and return early without error
        load_to_gsheet(df, "fake_spreadsheet_id")

    @patch('utils.load.Credentials.from_service_account_file', side_effect=FileNotFoundError)
    def test_load_to_gsheet_credential_file_not_found(self, mock_creds):
        df = pd.DataFrame({
            "Title": ["Kaos"],
            "Price": [50000]
        })
        load_to_gsheet(df, "fake_spreadsheet_id")

    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_load_to_gsheet_spreadsheet_not_found(self, mock_creds, mock_authorize):
        mock_creds.return_value = MagicMock()
        mock_client = MagicMock()
        mock_authorize.return_value = mock_client
        mock_client.open_by_key.side_effect = Exception("SpreadsheetNotFound")

        df = pd.DataFrame({
            "Title": ["Kaos"],
            "Price": [50000]
        })

        load_to_gsheet(df, "wrong_spreadsheet_id")

if __name__ == "__main__":
    unittest.main()
