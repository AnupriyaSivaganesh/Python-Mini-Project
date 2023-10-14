from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json

import foods_dao
import orders_dao
import quantity_dao

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getQuantity', methods=['GET'])
def get_quantity():
    response = quantity_dao.get_quantitys(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getFoods', methods=['GET'])
def get_foods():
    response = foods_dao.get_all_foods(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertFood', methods=['POST'])
def insert_food():
    request_payload = json.loads(request.form['data'])
    food_id = foods_dao.insert_new_food(connection, request_payload)
    response = jsonify({
        'food_id': food_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteFood', methods=['POST'])
def delete_food():
    return_id = foods_dao.delete_food(connection, request.form['food_id'])
    response = jsonify({
        'food_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Food Store Management System")
    app.run(port=5000)
