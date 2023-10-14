from datetime import datetime
from sql_connection import get_sql_connection
def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO of.orders "
             "(customer_name, total, date_time)"
             "VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO of.order_details "
                           "(order_id, product_id, quantity, total)"
                           "VALUES (%s, %s, %s, %s)")
    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['food_id']),
            float(order_detail_record['unit']),
            float(order_detail_record['total'])
        ])


    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id


def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from of.order_details where of.order_id = %s"

    query = "SELECT of.order_details.order_id, of.order_details.unit, of.order_details.total, "\
            "of.foods.name, of.foods.price_per_quantity FROM of.order_details LEFT JOIN of.foods on " \
            "of.order_details.food_id = of.foods.food_id where of.order_details.order_id = %s"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, unit, total, food_name, price_per_quantity) in cursor:
        records.append({
            'order_id': order_id,
            'unit': unit,
            'total': total,
            'food_name': food_name,
            'price_per_quantity': price_per_quantity
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM of.orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'date_time': dt,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(get_order_details(connection,4))
    # print(insert_order(connection, {
    #     'customer_name': 'dhaval',
    #     'total': '150',
    #     'datetime': datetime.now(),
    #     'order_details': [
    #         {
    #             'product_id': 1,
    #             'unit': 2,
    #             'total_price': 140
    #         },
    #         {
    #             'product_id': 3,
    #             'unit': 1,
    #             'total_price': 10
    #         }
    #     ]
    # }))
