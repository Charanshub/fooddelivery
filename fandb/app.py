# Simple Food Delivery App

menu = {
    "1": {"name": "Pizza", "price": 10},
    "2": {"name": "Burger", "price": 5},
    "3": {"name": "Pasta", "price": 8},
    "4": {"name": "Salad", "price": 4}
}

cart = []
orders = []

def show_menu():
    print("\n=== MENU ===")
    for id, item in menu.items():
        print(f"{id}. {item['name']} - ${item['price']}")

def add_to_cart():
    show_menu()
    choice = input("Enter item number: ")
    if choice in menu:
        qty = int(input("Quantity: "))
        cart.append({
            "name": menu[choice]["name"],
            "price": menu[choice]["price"],
            "quantity": qty
        })
        print(f"Added {qty}x {menu[choice]['name']} to cart!")
    else:
        print("Invalid choice!")

def view_cart():
    if not cart:
        print("Cart is empty!")
        return
    print("\n=== YOUR CART ===")
    total = 0
    for item in cart:
        cost = item["price"] * item["quantity"]
        total += cost
        print(f"{item['name']} x{item['quantity']} = ${cost}")
    print(f"Total: ${total}")

def checkout():
    if not cart:
        print("Cart is empty!")
        return
    view_cart()
    name = input("Enter your name: ")
    address = input("Enter address: ")
    orders.append({
        "customer": name,
        "address": address,
        "items": cart.copy(),
        "total": sum(i["price"] * i["quantity"] for i in cart)
    })
    cart.clear()
    print("Order placed successfully! 🎉")

def view_orders():
    if not orders:
        print("No orders yet!")
        return
    print("\n=== ORDERS ===")
    for i, order in enumerate(orders, 1):
        print(f"\nOrder #{i}")
        print(f"Customer: {order['customer']}")
        print(f"Address: {order['address']}")
        print(f"Total: ${order['total']}")

while True:
    print("\n=== FOOD DELIVERY ===")
    print("1. View Menu")
    print("2. Add to Cart")
    print("3. View Cart")
    print("4. Checkout")
    print("5. View Orders")
    print("6. Exit")
    
    choice = input("Choose (1-6): ")
    
    if choice == "1":
        show_menu()
    elif choice == "2":
        add_to_cart()
    elif choice == "3":
        view_cart()
    elif choice == "4":
        checkout()
    elif choice == "5":
        view_orders()
    elif choice == "6":
        print("Thanks for ordering!")
        break
    else:
        print("Invalid choice!")
