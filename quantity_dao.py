
def get_quantitys(connection):
    cursor = connection.cursor()
    query = ("select * from quantity")
    cursor.execute(query)
    response = []
    for (quantity_id, quantity_name) in cursor:
        response.append({
            'quantity_id': quantity_id,
            'quantity_name': quantity_name
        })
    return response


if __name__ == '__main__':
    from sql_connection import get_sql_connection

    connection = get_sql_connection()
    # print(get_all_products(connection))
    print(get_quantitys(connection))