import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import extract_products

class TestExtract(unittest.TestCase):

    @patch("utils.extract.requests.get")
    def test_extract_products_success(self, mock_get):
        html = '''
        <div class="collection-card">
            <h3 class="product-title">T-shirt</h3>
            <span class="price">$10.00</span>
            <div class="product-details">
                <p>Rating: ⭐ 4.5 / 5</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
                <p>Color: 2 Color</p>
            </div>
        </div>
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        products = extract_products(pages=1)
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 0)
        self.assertIn("name", products[0])
        self.assertIn("price", products[0])
        self.assertIn("rating", products[0])

if __name__ == "__main__":
    unittest.main()
