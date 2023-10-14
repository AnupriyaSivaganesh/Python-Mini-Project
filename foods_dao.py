from sql_connection import get_sql_connection

def get_all_foods(connection):
    cursor = connection.cursor()
    query = ("select of.foods.food_id, of.foods.name, of.foods.quantity_id, of.foods.price_per_quantity, of.quantity.quantity_name from of.foods inner join of.quantity on of.foods.quantity_id=of.quantity.quantity_id")
    cursor.execute(query)
    response = []
    for (food_id, name, quantity_id, price_per_quantity, quantity_name) in cursor:
        response.append({
            'food_id': food_id,
            'name': name,
            'quantity_id': quantity_id,
            'price_per_quantity': price_per_quantity,
            'quantity_name': quantity_name
        })
    return response

def insert_new_food(connection, food):
    cursor = connection.cursor()
    query = ("INSERT INTO of.foods "
             "(name, quantity_id, price_per_quantity)"
             "VALUES (%s, %s, %s)")
    data = (food['food_name'], food['quantity_id'], food['price_per_quantity'])

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_food(connection, food_id):
    cursor = connection.cursor()
    query = ("DELETE FROM of.foods where food_id=" + str(food_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_foods(connection))
    print(insert_new_food(connection, {
        'food_name': 'Veg fried rice',
        'quantity_id': '2',
        'price_per_quantity': 130
    }))
