from abc import ABC, abstractmethod  # Used for defining interfaces / abstract base classes
from datetime import datetime, timedelta  # Used for handling dates (expiry checks)
from typing import List  # Used for type annotations (list of items)


class Shippable(ABC):# Interface for products that can be shipped
    @abstractmethod
    def getName(self) -> str:# Must return product name
        pass

    @abstractmethod
    def getWeight(self) -> float:# Must return product weight
        pass


class Product(ABC):# Abstract base class for all products
    def __init__(self, name, price, quantity): # Constructor for common product data
        self.name = name
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def is_available(self):# Checks if product is available to sell
        pass


class PerishableProduct(Product): # Products that expire (e.g., milk, cheese)
    def __init__(self, name, price, quantity, expiry_date):
        super().__init__(name, price, quantity)
        self.expiry_date = expiry_date# Date when the product expires

    def is_available(self):# Available only if in stock and not expired
        return self.quantity > 0 and datetime.now() < self.expiry_date

    def is_expired(self): # Checks if the product has expired
        return datetime.now() >= self.expiry_date


class NonPerishableProduct(Product):# Products that don’t expire (e.g., electronics)
    def is_available(self):# Only needs to check stock
        return self.quantity > 0


class ShippablePerishableProduct(PerishableProduct, Shippable):
    def __init__(self, name, price, quantity, expiry_date, weight):
        super().__init__(name, price, quantity, expiry_date)
        self.weight = weight # Used for calculating shipping cost

    def getName(self):# Returns name for shipping label
        return self.name

    def getWeight(self):# Returns weight for shipping cost
        return self.weight


class ShippableNonPerishableProduct(NonPerishableProduct, Shippable):
    def __init__(self, name, price, quantity, weight):
        super().__init__(name, price, quantity)
        self.weight = weight

    def getName(self):# Returns name for shipping label
        return self.name

    def getWeight(self):# Returns weight for shipping cost
        return self.weight


class CartItem: # Represents one item in the shopping cart
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total_price(self):# Total price = price × quantity
        return self.product.price * self.quantity


class ShoppingCart:# Stores all cart items for a customer
    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, product, quantity):# Adds item to the cart
        # Check availability
        if not product.is_available():
            if isinstance(product, PerishableProduct) and product.is_expired():
                raise ValueError(f"{product.name} is expired.")
            raise ValueError(f"{product.name} is out of stock.")

         # Check stock quantity
        if quantity > product.quantity:
            raise ValueError(f"Only {product.quantity} units available for {product.name}.")
        # Update if already in cart
        for item in self.items:
            if item.product.name == product.name:
                if item.quantity + quantity > product.quantity:
                    raise ValueError(f"Not enough stock for {product.name}.")
                item.quantity += quantity
                return
        # Add new item
        self.items.append(CartItem(product, quantity))

    def is_empty(self): # Returns True if cart is empty
        return len(self.items) == 0

    def get_subtotal(self):# Total price without shipping
        return sum(item.get_total_price() for item in self.items)

    def get_shippable_items(self):  # Extracts all shippable products
        result = []
        for item in self.items:
            if isinstance(item.product, Shippable):
                result.extend([item.product] * item.quantity)
        return result

    def clear(self): # Empties the cart
        self.items.clear()


class Customer:# Represents a user with a balance and a cart
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.cart = ShoppingCart()

    def add_to_cart(self, product, quantity): # Adds to user's cart
        self.cart.add_item(product, quantity)

    def deduct_balance(self, amount):# Deducts money when purchasing
        if self.balance < amount:
            raise ValueError(f"Not enough balance. Needed: ${amount:.2f}, Available: ${self.balance:.2f}")
        self.balance -= amount


class ShippingService:  # Handles cost + shipping notice
    @staticmethod
    def calculate_shipping_fee(items, subtotal):# Calculates cost based on weight
        if not items or subtotal > 100:
            return 0.0
        total_weight = sum(item.getWeight() for item in items)
        return max(5.0, total_weight * 2.0)

    @staticmethod
    def ship_items(items):  # Print shipping details
        print("\nShipment Notice")
        for item in items:
            print(f"{item.getName()} ({item.getWeight():.2f} kg)")
        total_weight = sum(item.getWeight() for item in items)
        print(f"Total package weight: {total_weight:.2f} kg\n")


class ECommerceSystem: # Core system for products, customers, and checkout
    def __init__(self):
        self.products = []
        self.customers = []

    def add_product(self, product): # Register product
        self.products.append(product)

    def add_customer(self, customer):# Register customer
        self.customers.append(customer)

    def checkout(self, customer): # Main checkout logic
        if customer.cart.is_empty():
            raise ValueError("Cart is empty.")

        for item in customer.cart.items:
            if not item.product.is_available():
                if isinstance(item.product, PerishableProduct) and item.product.is_expired():
                    raise ValueError(f"{item.product.name} is expired.")
                raise ValueError(f"{item.product.name} is not available.")
            if item.quantity > item.product.quantity:
                raise ValueError(f"Not enough stock for {item.product.name}.")

        subtotal = customer.cart.get_subtotal()
        shippable_items = customer.cart.get_shippable_items()
        shipping_fee = ShippingService.calculate_shipping_fee(shippable_items, subtotal)
        total = subtotal + shipping_fee

        customer.deduct_balance(total)

        for item in customer.cart.items:
            item.product.quantity -= item.quantity

        print("\nCheckout Receipt")
        for item in customer.cart.items:
            print(f"{item.product.name} x{item.quantity} = ${item.get_total_price():.2f}")
        print("---------------------------")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Shipping: ${shipping_fee:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Remaining balance: ${customer.balance:.2f}\n")

        if shippable_items:
            ShippingService.ship_items(shippable_items)

        customer.cart.clear()


def test_all_cases():
    print("\nTEST CASE 1: Successful checkout with shipping")
    try:
        system = ECommerceSystem()
        cheese = ShippablePerishableProduct("Cheese", 100, 5, datetime.now() + timedelta(days=5), 0.2)
        biscuits = ShippablePerishableProduct("Biscuits", 150, 3, datetime.now() + timedelta(days=10), 0.7)
        scratch_card = NonPerishableProduct("Scratch Card", 50, 10)

        customer = Customer("Ammar", 1000)
        system.add_product(cheese)
        system.add_product(biscuits)
        system.add_product(scratch_card)
        system.add_customer(customer)

        customer.add_to_cart(cheese, 2)
        customer.add_to_cart(biscuits, 1)
        customer.add_to_cart(scratch_card, 1)

        system.checkout(customer)
    except Exception as e:
        print(f"Error: {e}")

    print("\nTEST CASE 2: Expired product")
    try:
        system = ECommerceSystem()
        expired_milk = PerishableProduct("Expired Milk", 20, 2, datetime.now() - timedelta(days=1))
        customer = Customer("Sarah", 200)
        system.add_product(expired_milk)
        system.add_customer(customer)
        customer.add_to_cart(expired_milk, 1)
    except Exception as e:
        print(f"Expected Error: {e}")

    print("\nTEST CASE 3: Out of stock")
    try:
        system = ECommerceSystem()
        tv = ShippableNonPerishableProduct("TV", 300, 1, 5.0)
        customer = Customer("Ali", 1000)
        system.add_product(tv)
        system.add_customer(customer)
        customer.add_to_cart(tv, 2)
    except Exception as e:
        print(f"Expected Error: {e}")

    print("\nTEST CASE 4: Insufficient balance")
    try:
        system = ECommerceSystem()
        laptop = ShippableNonPerishableProduct("Laptop", 950, 1, 2.0)
        customer = Customer("Laila", 500)
        system.add_product(laptop)
        system.add_customer(customer)
        customer.add_to_cart(laptop, 1)
        system.checkout(customer)
    except Exception as e:
        print(f"Expected Error: {e}")

    print("\nTEST CASE 5: Free shipping (subtotal > 100)")
    try:
        system = ECommerceSystem()
        phone = ShippableNonPerishableProduct("Smartphone", 150, 2, 0.5)
        customer = Customer("Omar", 500)
        system.add_product(phone)
        system.add_customer(customer)
        customer.add_to_cart(phone, 1)
        system.checkout(customer)
    except Exception as e:
        print(f"Error: {e}")

    print("\nTEST CASE 6: Non-shippable only")
    try:
        system = ECommerceSystem()
        coupon = NonPerishableProduct("Gift Coupon", 30, 5)
        customer = Customer("Nour", 100)
        system.add_product(coupon)
        system.add_customer(customer)
        customer.add_to_cart(coupon, 2)
        system.checkout(customer)
    except Exception as e:
        print(f"Error: {e}")

    print("\nTEST CASE 7: Empty cart checkout")
    try:
        system = ECommerceSystem()
        customer = Customer("Mina", 200)
        system.add_customer(customer)
        system.checkout(customer)
    except Exception as e:
        print(f"Expected Error: {e}")


if __name__ == "__main__":
    test_all_cases()
