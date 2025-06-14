import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import extract_product_data, scrape_all_pages

class TestExtract(unittest.TestCase):

    def setUp(self):
        self.valid_html = '''
        <div class="collection-card">
            <h3 class="product-title">T-shirt</h3>
            <div class="price-container">$5.00</div>
            <div class="product-details">
                <p>Rating: ⭐ 4.5 / 5</p>
                <p>Color: 2 Color</p>
                <p>Size: L</p>
                <p>Gender: Men</p>
            </div>
        </div>
        '''
        self.soup = BeautifulSoup(self.valid_html, 'html.parser')
        self.product = self.soup.select_one('.collection-card')

    def test_extract_product_data_success(self):
        data = extract_product_data(self.product)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], "T-shirt")
        self.assertEqual(data['price'], 5.00)
        self.assertEqual(data['rating'], 4.5)
        self.assertEqual(data['color'], 2)
        self.assertEqual(data['size'], 'L')
        self.assertEqual(data['gender'], 'men')
        self.assertIn('timestamp', data)

    def test_extract_product_data_missing_fields(self):
        html = '''
        <div class="collection-card">
            <h3 class="product-title">No Price Product</h3>
            <div class="product-details">
                <p>Rating: 3 / 5</p>
            </div>
        </div>
        '''
        product = BeautifulSoup(html, 'html.parser').select_one('.collection-card')
        data = extract_product_data(product)
        self.assertEqual(data['price'], 0)
        self.assertEqual(data['color'], 0)
        self.assertEqual(data['size'], 'N/A')
        self.assertEqual(data['gender'], 'unisex')

    @patch("utils.extract.requests.get")
    def test_scrape_all_pages_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.valid_html
        mock_get.return_value = mock_response

        data = scrape_all_pages()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]['name'], 'T-shirt')

    @patch("utils.extract.requests.get")
    def test_scrape_all_pages_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        data = scrape_all_pages()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    @patch("utils.extract.requests.get")
    def test_scrape_all_pages_no_products(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><div>No products here</div></body></html>"
        mock_get.return_value = mock_response

        data = scrape_all_pages()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    @patch("utils.extract.requests.get")
    def test_scrape_all_pages_exception(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        data = scrape_all_pages()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

if __name__ == "__main__":
    unittest.main()
