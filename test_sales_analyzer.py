
import unittest
import tempfile
import os
import sales_analyzer

from sales_analyzer import (
    calculate_total_revenue,
    calculate_average_revenue,
    find_best_selling_product,
    find_best_selling_by_quantity,
    validate_products,
    read_products
)


class TestSalesAnalyzer(unittest.TestCase):

    def setUp(self):
        self.products = [
            {"product": "Laptop", "quantity": 2, "price": 100},
            {"product": "Mouse", "quantity": 3, "price": 50}
        ]
        self.temp_filename = None

    def tearDown(self):
        if self.temp_filename is not None:
            os.remove(self.temp_filename)

    def test_calculate_total_revenue(self):
       
        self.assertEqual(calculate_total_revenue(self.products), 350)

    def test_empty_products(self):
        self.assertEqual(calculate_total_revenue([]), 0)

    def test_total_revenue_with_zero_quantity(self):
        products = [
            {"product": "Laptop", "quantity": 2, "price": 100},
            {"product": "Mouse", "quantity": 3, "price": 50},
            {"product": "Keyboard", "quantity": 0, "price": 200}
        ]
        self.assertEqual(calculate_total_revenue(products), 350)

    def test_high_price_zero_quantity(self):
        products = [
            {"product": "Laptop", "quantity": 0, "price": 999999}
        ]
        self.assertEqual(calculate_total_revenue(products), 0)

    def test_zero_price(self):
        products = [
        {"product": "Laptop", "quantity": 1, "price": 0},
        {"product": "Mouse", "quantity": 5, "price": 0}
    ]
        self.assertEqual(calculate_total_revenue(products), 0)
        
    def test_negative_quantity_raises_error(self):
        invalid_values = [-2, -5]

        for quantity in invalid_values:
            with self.subTest(quantity=quantity):
                products = [
                {"product": "Laptop", "quantity": quantity, "price": 100}
            ]

                with self.assertRaises(ValueError):
                    calculate_total_revenue(products)
    

    def test_negative_price_raises_error(self):
        products = [
            {"product": "Laptop", "quantity": 2, "price": -100}
        ]
        with self.assertRaises(ValueError):
            calculate_total_revenue(products)


    # AVERAGE REVENUE TESTS

    def test_calculate_average_revenue(self):
    
        self.assertEqual(calculate_average_revenue(self.products), 175)

    def test_average_revenue_empty(self):
        self.assertIsNone(calculate_average_revenue([]))


    # BEST-SELLING PRODUCT TESTS

    def test_best_selling_product(self):
        result = find_best_selling_product(self.products)
        self.assertEqual(result["product name"], "Laptop")

    def test_best_selling_by_quantity(self):
        products = [
            {"product": "Laptop", "quantity": 2, "price": 100},
            {"product": "Mouse", "quantity": 3, "price": 50}
        ]
        result = find_best_selling_by_quantity(products)
        self.assertEqual(result["product"], "Mouse")

    def test_best_selling_product_empty(self):
        result = find_best_selling_product([])
        self.assertEqual(
            result,
            {"product name": None, "Highest revenue": 0}
        )

    def test_best_selling_by_quantity_empty(self):
        result = find_best_selling_by_quantity([])
        self.assertEqual(
            result,
            {"product": None, "quantity": 0}
        )


    # PRODUCT VALIDATION TESTS

    def test_valid_products(self):
        products = [
            {"product": "Laptop", "quantity": 2, "price": 100},
            {"product": "Mouse", "quantity": 3, "price": 50}
        ]
        self.assertTrue(validate_products(products))

    def test_invalid_products(self):
        products = [
            {"product": "Laptop", "quantity": 2, "price": 100},
            {"product": "Mouse", "quantity": -3, "price": 50}
        ]
        self.assertFalse(validate_products(products))

    def test_empty_product_validation(self):
        self.assertFalse(validate_products([]))


    # CSV TESTS

    def test_missing_csv_file(self):
        result = read_products("missing_file.csv")
        self.assertEqual(result, [])

    def test_invalid_numeric_data(self):
        with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False
    ) as file:
            file.write("product,quantity,price\n")
            file.write("Laptop,abc,100\n")
            file.write("Mouse,3,50\n")
            self.temp_filename = file.name

        result = read_products(self.temp_filename)
        expected = [
        {"product": "Mouse", "quantity": 3, "price": 50}
    ]
        self.assertEqual(result, expected)

    def test_missing_product_name(self):
        with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False
    ) as file:
            file.write("product,quantity,price\n")
            file.write(",2,100\n")
            file.write("Mouse,3,50\n")
            self.temp_filename = file.name

        result = read_products(self.temp_filename)
        expected = [
        {"product": "Mouse", "quantity": 3, "price": 50}
    ]
        self.assertEqual(result, expected)
        

    def test_negative_quantity(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as file:
            file.write("product,quantity,price\n")
            file.write("Laptop,-2,100\n")
            file.write("Mouse,3,50\n")
            self.temp_filename = file.name

        result = read_products(self.temp_filename)
        expected = [
                {"product": "Mouse", "quantity": 3, "price": 50}
            ]
        self.assertEqual(result, expected)
        

    def test_negative_price(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as file:
            file.write("product,quantity,price\n")
            file.write("Laptop,2,-100\n")
            file.write("Mouse,3,50\n")
            self.temp_filename = file.name

        result = read_products(self.temp_filename)
        expected = [
                {"product": "Mouse", "quantity": 3, "price": 50}
            ]
        self.assertEqual(result, expected)
        

    def test_read_temporary_csv(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as file:
            file.write("product,quantity,price\n")
            file.write("Laptop,2,100\n")
            self.temp_filename = file.name

      
        result = read_products(self.temp_filename)
        expected = [
                {"product": "Laptop", "quantity": 2, "price": 100}
            ]
        self.assertEqual(result, expected)

            

    def test_empty_csv(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as file:
            file.write("product,quantity,price\n")
            self.temp_filename = file.name

        result = read_products(self.temp_filename)
        self.assertEqual(result, [])
      
    def test_missing_headers(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as file:
            file.write("item,count,cost\n")
            file.write("Laptop,2,100\n")
            self.temp_filename = file.name
        result = read_products(self.temp_filename)
        self.assertEqual(result, [])
        

    

    def test_zero_quantity_one(self):
       products=[{"product": "Laptop", "quantity": 0, "price":500} ]
       self.assertEqual(calculate_average_revenue(products),0)

    def test_average_revenue_multiple_products(self):
       products=[{"product": "Laptop", "quantity": 2, "price":100},
                 {"product": "Mouse", "quantity": 3, "price":50},
                 {"product": "Keyboard", "quantity": 1, "price":200}]
       self.assertAlmostEqual(calculate_average_revenue(products),550 / 3)

    def test_average_revenue_dict(self):
        products = {}
        with self.assertRaises(TypeError):
            calculate_average_revenue(products)
        
    def test_none(self):
        products = None
        with self.assertRaises(TypeError):
            calculate_average_revenue(products)


    def test_temporary_file_cleanup(self):
        with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False
    ) as file:
            file.write("product,quantity,price\n")
            file.write("Laptop,2,100\n")
            self.temp_filename = file.name

        self.assertTrue(os.path.exists(self.temp_filename))

    

    

    def test_zero_quantity_valid(self):
        
        products=[{"product": "Laptop", "quantity": 0, "price": 500}]
        self.assertEqual(calculate_total_revenue(products),0)

    def test_invalid_quantity_type(self):
        products = [
        {"product": "Laptop", "quantity": "two", "price": 500}
    ]

        with self.assertRaises(ValueError):
            calculate_total_revenue(products)

    def test_invalid_quantities(self):
        invalid_values = ["two", -5, 10.5]

        for quantity in invalid_values:
            with self.subTest(quantity=quantity):
                products = [
                {"product": "Laptop", "quantity": quantity, "price": 500}
            ]

                with self.assertRaises((ValueError, TypeError)):
                    calculate_total_revenue(products)
           

if __name__ == "__main__":
    unittest.main()
