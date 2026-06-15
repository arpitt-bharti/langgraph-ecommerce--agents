import sqlite3

def fetch_order_from_db(order_id : str) :
    conn = sqlite3.connect('orderss.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """ 
        select * from orderss where order_id = ?
        """,(order_id,)
        )
    res = cursor.fetchone()
    if res:
        return dict(res)
    else:
        return 'no order found !'