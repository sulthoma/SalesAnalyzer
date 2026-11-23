import csv


def read_products(filename):
    """Read and validate product rows from a CSV file."""
    products = []
    try:
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                print("CSV file is empty or missing headers.")
                return []
            required_columns = ["product", "quantity", "price"]
            for column in required_columns:
                if column not in reader.fieldnames:
                    print(f"Missing column: {column}")
                    return []
            for row in reader:
                if not row["product"].strip():
                    print("Product name is missing. Skipping row.")
                    continue
                if row["quantity"] == "" or row["price"] == "":
                    print("Quantity or price is missing. Skipping row.")
                    continue
                try:
                    quantity = int(row["quantity"])
                    price = int(row["price"])
                except ValueError:
                    print("Invalid quantity or price. Skipping this product.")
                    continue
                if quantity < 0 or price < 0:
                    print("Quantity and price cannot be negative. Skipping row.")
                    continue
                row["product"] = row["product"].strip()
                row["quantity"] = quantity
                row["price"] = price
                products.append(row)
    except FileNotFoundError:
        print("CSV file not found.")
    return products


def validate_product_name(products):
    if not products:
        return False
    for row in products:
        if not row["product"].strip():
            return False
    return True


def validate_quantity(products):
    if not products:
        return False
    for row in products:
        if type(row["quantity"]) != int or row["quantity"] < 0:
            return False
    return True


def validate_price(products):
    if not products:
        return False
    for row in products:
        if type(row["price"]) != int or row["price"] < 0:
            return False
    return True


def validate_products(products):
    return (validate_product_name(products)
            and validate_quantity(products)
            and validate_price(products))


def calculate_total_revenue(products):
    if not products:
        return 0
    if not validate_products(products):
        raise ValueError("Invalid product data.")
    total_revenue = 0
    for row in products:
        total_revenue += row["quantity"] * row["price"]
    return total_revenue


def find_best_selling_product(products):
    high_revenue = 0
    best_product = None
    for row in products:
        revenue = row["quantity"] * row["price"]
        if revenue > high_revenue:
            high_revenue = revenue
            best_product = row["product"]
    return {"product name": best_product, "Highest revenue": high_revenue}


def find_best_selling_by_quantity(products):
    high_quantity = 0
    high_product = None
    for row in products:
        quantity = row["quantity"]
        if quantity > high_quantity:
            high_quantity = quantity
            high_product = row["product"]
    return {"product": high_product, "quantity": high_quantity}


def calculate_average_revenue(products):
    if not isinstance(products, list):
        raise TypeError("products must be a list")

    if not products:
        return None

    total_revenue = 0
    for row in products:
        total_revenue += row["quantity"] * row["price"]

    return total_revenue / len(products)


def single_loop_calc(products):
    total_revenue = 0
    high_revenue = 0
    best_product = None
    high_quantity = 0
    high_product = None
    for row in products:
        quantity = row["quantity"]
        price = row["price"]
        revenue = quantity * price
        total_revenue += revenue
        if revenue > high_revenue:
            high_revenue = revenue
            best_product = row["product"]
        if quantity > high_quantity:
            high_quantity = quantity
            high_product = row["product"]
    return {
        "total_revenue": total_revenue,
        "best_selling_product": best_product,
        "best_selling_by_quantity": high_product,
        "highest_revenue": high_revenue,
        "highest_quantity": high_quantity
    }


def sort_products_by_revenue(products):
    sales = []
    for row in products:
        revenue = row["quantity"] * row["price"]
        sales.append((row["product"], revenue))
    return sorted(sales, key=lambda item: item[1], reverse=True)


def find_top_2_products(products):
    return sort_products_by_revenue(products)[:2]


def find_top_2_products_by_quantity(products):
    """Return the names of the two products with the highest quantities."""
    sorted_products = sorted(products, key=lambda row: row["quantity"], reverse=True)
    return [row["product"] for row in sorted_products[:2]]


def find_top_3_products(products):
    return sort_products_by_revenue(products)[:3]


def find_top_products(products, n):
    return sort_products_by_revenue(products)[:n]


def rank_products(products):
    sorted_products = sort_products_by_revenue(products)
    return [(rank, product, revenue)
            for rank, (product, revenue) in enumerate(sorted_products, start=1)]


def print_rankings(products):
    print("========== PRODUCT RANKING ==========")
    for rank, product, revenue in rank_products(products):
        print(f"{rank}. {product} - ₹{revenue}")


def generate_sales_report(products):
    return {
        "total_revenue": calculate_total_revenue(products),
        "best_selling_product": find_best_selling_product(products),
        "best_selling_by_quantity": find_best_selling_by_quantity(products),
        "average_revenue": calculate_average_revenue(products),
        "total_products": len(products),
        "product_ranking": rank_products(products)
    }


def print_sales_report(report):
    print("================ SALES REPORT ================")
    print("Total Revenue: ₹", report["total_revenue"])
    average_revenue = report["average_revenue"]
    if average_revenue is None:
        print("Average Revenue: N/A")
    else:
        print("Average Revenue: ₹", round(average_revenue, 2))
    print("Total products:", report["total_products"])
    best_product = report["best_selling_product"]
    if best_product["product name"] is None:
        print("Best selling product: N/A")
    else:
        print("Best selling product:", best_product["product name"])
        print("Highest revenue: ₹", best_product["Highest revenue"])
    best_quantity = report["best_selling_by_quantity"]
    if best_quantity["product"] is None:
        print("Best selling quantity: N/A")
    else:
        print("Best selling quantity by product:", best_quantity["product"])
        print("Best selling quantity:", best_quantity["quantity"])
    print("\n============= PRODUCT RANKING ===============")
    if not report["product_ranking"]:
        print("No products to rank.")
    else:
        for rank, product, revenue in report["product_ranking"]:
            print(f"{rank}. {product} - ₹{revenue}")
    print("==============================================")


if __name__ == "__main__":
    products = read_products("products.csv")
    report = generate_sales_report(products)
    print_sales_report(report)

# Project update: Practising Git version control
# Feature branch: Working on report export
# Feature branch: Sales summary report