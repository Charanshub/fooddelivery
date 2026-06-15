from flask import Flask, render_template_string, request

app = Flask(__name__)

menu = {
    "1": {"name": "Pizza", "price": 10},
    "2": {"name": "Burger", "price": 5}
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Food Delivery</title></head>
<body>
    <h1>Food Delivery App</h1>
    <h2>Menu</h2>
    <ul>
    {% for id, item in menu.items() %}
        <li>{{ item.name }} - ${{ item.price }}</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, menu=menu)

@app.route('/menu')
def menu_api():
    return menu

if __name__ == '__main__':
    # Change port number here
    PORT = 5000  # Modify this number as needed
    
    print(f"App running on: http://localhost:{PORT}")
    print(f"Menu available at: http://localhost:{PORT}/menu")
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
