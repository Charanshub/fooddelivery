from flask import Flask, render_template_string, request, session, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'food_delivery_secret_key_2024'

# Menu Data
menu = {
    1: {"name": "Margherita Pizza", "price": 12.99, "category": "Pizza", "image": "🍕"},
    2: {"name": "Cheeseburger", "price": 8.99, "category": "Burger", "image": "🍔"},
    3: {"name": "Chicken Wings", "price": 10.99, "category": "Appetizer", "image": "🍗"},
    4: {"name": "Caesar Salad", "price": 7.99, "category": "Salad", "image": "🥗"},
    5: {"name": "Pasta Alfredo", "price": 13.99, "category": "Pasta", "image": "🍝"},
    6: {"name": "Coca Cola", "price": 2.49, "category": "Beverage", "image": "🥤"},
    7: {"name": "French Fries", "price": 3.99, "category": "Sides", "image": "🍟"},
    8: {"name": "Ice Cream", "price": 4.99, "category": "Dessert", "image": "🍦"}
}

orders = []

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Food Delivery App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        h1 {
            color: #667eea;
            font-size: 2.5em;
        }
        
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .menu-item {
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        .menu-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 25px rgba(0,0,0,0.2);
        }
        
        .menu-emoji {
            font-size: 4em;
        }
        
        .menu-name {
            font-size: 1.3em;
            font-weight: bold;
            margin: 10px 0;
            color: #333;
        }
        
        .menu-price {
            color: #667eea;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .menu-category {
            color: #999;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .add-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
            transition: background 0.3s;
        }
        
        .add-btn:hover {
            background: #764ba2;
        }
        
        .cart-section {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        .cart-item {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        
        .checkout-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.1em;
            margin-top: 15px;
        }
        
        .checkout-btn:hover {
            background: #218838;
        }
        
        .order-list {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .order-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px;
            border-radius: 5px;
            display: none;
            z-index: 1000;
        }
        
        .cart-total {
            font-size: 1.2em;
            font-weight: bold;
            text-align: right;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 2px solid #ddd;
        }
        
        .btn-clear {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        
        input, select {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍕 Food Delivery App 🚚</h1>
            <p>Delicious food delivered to your doorstep!</p>
        </header>
        
        <div class="menu-grid">
            {% for id, item in menu.items() %}
            <div class="menu-item" onclick="addToCart({{ id }})">
                <div class="menu-emoji">{{ item.image }}</div>
                <div class="menu-name">{{ item.name }}</div>
                <div class="menu-price">${{ "%.2f"|format(item.price) }}</div>
                <div class="menu-category">{{ item.category }}</div>
                <button class="add-btn" onclick="event.stopPropagation(); addToCart({{ id }})">Add to Cart</button>
            </div>
            {% endfor %}
        </div>
        
        <div class="cart-section">
            <h2>🛒 Your Cart</h2>
            <div id="cart-items"></div>
            <div id="cart-total" class="cart-total"></div>
            <button class="btn-clear" onclick="clearCart()">Clear Cart</button>
            <button class="checkout-btn" onclick="checkout()">Proceed to Checkout</button>
        </div>
        
        <div class="order-list">
            <h2>📋 Recent Orders</h2>
            <div id="orders-list"></div>
        </div>
    </div>
    
    <div id="notification" class="notification"></div>
    
    <script>
        let cart = {};
        
        function addToCart(itemId) {
            fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({item_id: itemId})
            })
            .then(response => response.json())
            .then(data => {
                showNotification(data.message);
                updateCartDisplay();
            });
        }
        
        function updateCartDisplay() {
            fetch('/get_cart')
                .then(response => response.json())
                .then(data => {
                    const cartDiv = document.getElementById('cart-items');
                    const totalDiv = document.getElementById('cart-total');
                    
                    if (Object.keys(data.cart).length === 0) {
                        cartDiv.innerHTML = '<p>Your cart is empty</p>';
                        totalDiv.innerHTML = '';
                        return;
                    }
                    
                    let html = '';
                    let total = 0;
                    
                    for (let id in data.cart) {
                        const item = data.cart[id];
                        const subtotal = item.price * item.quantity;
                        total += subtotal;
                        html += `
                            <div class="cart-item">
                                <span>${item.name} x${item.quantity}</span>
                                <span>$${subtotal.toFixed(2)}</span>
                            </div>
                        `;
                    }
                    
                    cartDiv.innerHTML = html;
                    totalDiv.innerHTML = `Total: $${total.toFixed(2)}`;
                });
        }
        
        function clearCart() {
            fetch('/clear_cart', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    showNotification(data.message);
                    updateCartDisplay();
                });
        }
        
        function checkout() {
            const name = prompt('Enter your name:');
            if (!name) return;
            
            const address = prompt('Enter delivery address:');
            if (!address) return;
            
            const phone = prompt('Enter phone number:');
            if (!phone) return;
            
            fetch('/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    address: address,
                    phone: phone
                })
            })
            .then(response => response.json())
            .then(data => {
                showNotification(data.message);
                updateCartDisplay();
                loadOrders();
            });
        }
        
        function loadOrders() {
            fetch('/get_orders')
                .then(response => response.json())
                .then(data => {
                    const ordersDiv = document.getElementById('orders-list');
                    if (data.orders.length === 0) {
                        ordersDiv.innerHTML = '<p>No orders yet</p>';
                        return;
                    }
                    
                    let html = '';
                    data.orders.slice().reverse().forEach(order => {
                        html += `
                            <div class="order-item">
                                <strong>Order #${order.id}</strong><br>
                                Customer: ${order.customer}<br>
                                Total: $${order.total.toFixed(2)}<br>
                                Status: ${order.status}<br>
                                Time: ${order.time}
                            </div>
                        `;
                    });
                    ordersDiv.innerHTML = html;
                });
        }
        
        function showNotification(message) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.style.display = 'block';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 2000);
        }
        
        // Load initial data
        updateCartDisplay();
        loadOrders();
        
        // Auto-refresh cart every 5 seconds
        setInterval(updateCartDisplay, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, menu=menu)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    item_id = str(data['item_id'])
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if item_id in session['cart']:
        session['cart'][item_id]['quantity'] += 1
    else:
        session['cart'][item_id] = {
            'name': menu[int(item_id)]['name'],
            'price': menu[int(item_id)]['price'],
            'quantity': 1
        }
    
    session.modified = True
    return {'message': f"Added {menu[int(item_id)]['name']} to cart!"}

@app.route('/get_cart')
def get_cart():
    cart = session.get('cart', {})
    return {'cart': cart}

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    session.modified = True
    return {'message': 'Cart cleared!'}

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    cart = session.get('cart', {})
    
    if not cart:
        return {'message': 'Cart is empty!'}
    
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    order = {
        'id': len(orders) + 1,
        'customer': data['name'],
        'address': data['address'],
        'phone': data['phone'],
        'items': cart,
        'total': total,
        'status': 'Placed',
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    orders.append(order)
    session['cart'] = {}
    session.modified = True
    
    return {'message': f'Order placed successfully! Order #{order["id"]}'}

@app.route('/get_orders')
def get_orders():
    return {'orders': orders}

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🍕 FOOD DELIVERY APP IS RUNNING! 🚚")
    print("="*50)
    print(f"📍 Access the app at: http://localhost:5000")
    print(f"📍 Or: http://127.0.0.1:5000")
    print("="*50)
    print("Press CTRL+C to stop the server")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
