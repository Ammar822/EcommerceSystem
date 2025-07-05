# Simple E-Commerce System (Python)

This is a basic e-commerce simulation written in Python. It models real-life shopping features like products (perishable/non-perishable), customer carts, shipping fees, and checkout handling.

## Features

* Add perishable and non-perishable products
* Add items to a customer's cart
* Handle expired products and out-of-stock errors
* Calculate shipping fees based on weight
* Print a detailed checkout receipt
* Includes test cases to cover success and failure scenarios

## Code Overview

* `Product` is the abstract base class for all products
* `PerishableProduct` and `NonPerishableProduct` extend `Product`
* `Shippable` is an interface for shipping-related methods
* `ShippablePerishableProduct` and `ShippableNonPerishableProduct` implement the interface
* `ShoppingCart` holds items and calculates subtotal
* `Customer` holds balance and cart
* `ShippingService` calculates shipping fees and prints shipment details
* `ECommerceSystem` connects everything and manages checkout logic
* `test_all_cases()` runs multiple test cases

## How to Run

1. Make sure you have Python 3 installed.
2. Save the code in a file like `main.py`.
3. Open your terminal in the folder containing the file.
4. Run the file:

```bash
python main.py
```

## Sample Output

```
Checkout Receipt
Cheese x2 = $200.00
Biscuits x1 = $150.00
Scratch Card x1 = $50.00
---------------------------
Subtotal: $400.00
Shipping: $30.00
Total: $430.00
Remaining balance: $570.00

Shipment Notice
Cheese (0.20 kg)
Cheese (0.20 kg)
Biscuits (0.70 kg)
Total package weight: 1.10 kg
```

## Test Cases Included

* ✅ Successful checkout with shipping
* ✅ Free shipping if subtotal > \$100
* ✅ Checkout with only non-shippable items
* ❌ Expired product cannot be added
* ❌ Adding more than available stock
* ❌ Insufficient customer balance
* ❌ Checkout when cart is empty

## Author

Ammar Mohamed
