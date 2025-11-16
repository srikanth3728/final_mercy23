from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'foodapp')

try:
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    menu_collection = db['menu']
    orders_collection = db['orders']
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"⚠️ MongoDB error: {e}")

# Initialize default menu
def init_menu():
    if menu_collection.count_documents({}) == 0:
        default_menu = [
            {"name": "Chicken Biryani", "description": "Fragrant basmati rice cooked with tender chicken and aromatic spices", "price": 250, "emoji": "🍛"},
            {"name": "Margherita Pizza", "description": "Classic pizza with fresh mozzarella, tomato sauce, and basil", "price": 300, "emoji": "🍕"},
            {"name": "Cheese Burger", "description": "Juicy beef patty with cheese, lettuce, tomato, and special sauce", "price": 180, "emoji": "🍔"},
            {"name": "Creamy Pasta", "description": "Penne pasta in rich white sauce with mushrooms and herbs", "price": 220, "emoji": "🍝"},
            {"name": "Caesar Salad", "description": "Fresh romaine lettuce with caesar dressing, croutons, and parmesan", "price": 150, "emoji": "🥗"},
            {"name": "Chocolate Brownie", "description": "Warm chocolate brownie with vanilla ice cream", "price": 120, "emoji": "🍰"}
        ]
        menu_collection.insert_many(default_menu)
        print("✅ Menu initialized")

# API Routes
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        items = list(menu_collection.find({}, {'_id': 1, 'name': 1, 'description': 1, 'price': 1, 'emoji': 1}))
        for item in items:
            item['id'] = str(item['_id'])
            del item['_id']
        return jsonify({"success": True, "data": items})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.json
        order = {
            "customerName": data.get('customerName'),
            "customerPhone": data.get('customerPhone'),
            "customerAddress": data.get('customerAddress'),
            "deliveryTime": data.get('deliveryTime'),
            "items": data.get('items', []),
            "total": data.get('total', 0),
            "status": "pending",
            "createdAt": datetime.now().isoformat()
        }
        result = orders_collection.insert_one(order)
        return jsonify({"success": True, "orderId": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = list(orders_collection.find({}).sort("createdAt", -1).limit(50))
        for order in orders:
            order['_id'] = str(order['_id'])
        return jsonify({"success": True, "data": orders})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    init_menu()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

