import unittest
from parser import extract_price

MOCK_HTML = """
<html>
<body>
    <div class="product_main">
        <h1>A Light in the Attic</h1>
        <p class="price_color">£51.77</p>
        <p class="instock availability">In stock</p>
    </div>
</body>
</html>
"""

INVALID_HTML = """
<html><body><div>No price here</div></body></html>
"""

class ParserTests(unittest.TestCase):
    def test_extract_price_success(self) -> None:
        price = extract_price(MOCK_HTML)
        self.assertEqual(price, 51.77)

    def test_extract_price_fails_gracefully(self) -> None:
        with self.assertRaises(ValueError):
            extract_price(INVALID_HTML)

if __name__ == "__main__":
    unittest.main()