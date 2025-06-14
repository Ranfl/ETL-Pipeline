import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import transform_products

class TestTransform(unittest.TestCase):

    def test_transform_products_cleaning(self):
        sample = [{
            "name": "  Kaos ",
            "price": 50000,
            "rating": 4.5,
            "size": "l",
            "gender": "Male",
            "color": "2 Color"
        }]
        df = transform_products(sample)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.iloc[0]["Title"], "Kaos")
        self.assertEqual(df.iloc[0]["Gender"], "male")
        self.assertEqual(df.iloc[0]["Size"], "L")
        self.assertEqual(df.iloc[0]["Colors"], 2)

    def test_transform_products_filter(self):
        sample = [
            {"name": "", "price": 50000, "rating": 4.5, "size": "L", "gender": "male", "color": "1"},  # invalid name
            {"name": "Kaos", "price": -100, "rating": 4.5, "size": "L", "gender": "male", "color": "2"},  # invalid price
        ]
        df = transform_products(sample)
        self.assertEqual(len(df), 0)

if __name__ == "__main__":
    unittest.main()
