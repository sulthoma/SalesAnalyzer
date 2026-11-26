import unittest
import tempfile
import os
import csv
import sales_analyzer

from sales_analyzer import (
    calculate_total_revenue,
    calculate_average_revenue,
    find_best_selling_product,
    find_best_selling_by_quantity,
    validate_products,
    read_products,
    sort_products_by_revenue,
    generate_sales_report
)

class TestSalesAnalyzer(unittest.TestCase):

    def setUp(self):
        self.products = [
            {"product": "Laptop", "quantity": 2, "price": 100},
            {"product": "Mouse", "quantity": 3, "price": 50}
        ]
        self.temp_filename = None

    def tearDown(self):
        if self.temp_filename is not None and os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_sort_products_by_revenue_with_tie(self):
        products = [
            {"product": "Laptop", "quantity": 2, "price": 500},
            {"product": "Monitor", "quantity": 1, "price": 1000},
            {"product": "Mouse", "quantity": 3, "price": 20}
        ]

        result = sort_products_by_revenue(products)
        self.assertEqual(
            result,
            [("Laptop", 1000), ("Monitor", 1000), ("Mouse", 60)]
        )

    def test_export_product_ranking_to_csv(self):
        report = generate_sales_report(self.products)

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".csv",
            newline="",
            delete=False
        ) as file:
            self.temp_filename = file.name

        sales_analyzer.export_product_ranking_to_csv(
            report,
            self.temp_filename
        )

        with open(
            self.temp_filename,
            mode="r",
            newline=""
        ) as file:
            rows = list(csv.reader(file))

        expected_rows = [
            ["rank", "product", "revenue"],
            ["1", "Laptop", "200"],
            ["2", "Mouse", "150"]
        ]

        self.assertEqual(rows, expected_rows)

if __name__ == "__main__":
    unittest.main()