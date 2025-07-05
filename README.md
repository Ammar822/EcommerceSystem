

````markdown
# Simple E-Commerce System (Python)

This is a basic e-commerce simulation written in Python. It includes product types (like perishable and non-perishable), a shopping cart, a customer class, and shipping logic.

## Features

- Add perishable and non-perishable products
- Add items to a customer's cart
- Handle expired products and out-of-stock errors
- Calculate shipping fees based on weight
- Print a detailed checkout receipt
- Includes test cases to cover common scenarios

## Structure

- `Product` classes (base, perishable, non-perishable)
- `Shippable` interface for shipping logic
- `Customer` class with balance and cart
- `ShoppingCart` class for handling items
- `ShippingService` for fee calculation and shipment notice
- `ECommerceSystem` for managing everything
- `test_all_cases()` to run demo/test cases

## How to Run

1. Make sure you have Python 3 installed.
2. Clone this repo or copy the files to your machine.
3. Run the main file (the one with `test_all_cases()`):

```bash
python products.py
````

## Example Output

```
Checkout Receipt
Cheese x2 = $200.00
Biscuits x1 = $150.00
---------------------------
Subtotal: $350.00
Shipping: $30.00
Total: $380.00
Remaining balance: $620.00

Shipment Notice
Cheese (0.20 kg)
Cheese (0.20 kg)
Biscuits (0.70 kg)
Total package weight: 1.10 kg
```

## Author

Ammar Mohamed

```

---


```
