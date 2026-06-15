import sqlite3
import json

with open('orders.json', 'r', encoding='utf-8') as order:
    orders = json.load(order)

conn = sqlite3.connect('orderss.db')
if conn:
    print('DB created successfully !')

cursor = conn.cursor()

cursor.execute(
    """ 
    CREATE TABLE IF NOT EXISTS orderss (
    order_id                TEXT    PRIMARY KEY,
    customer_name           TEXT,
    order_date              DATE,
    amount                  REAL,
    payment_status          TEXT,
    payment_method          TEXT,
    payment_transaction_id  TEXT,
    payment_error_code      TEXT,
    shipping_status         TEXT,
    tracking_number         TEXT,
    estimated_delivery      DATE,
    delivery_date           DATE,
    refund_status           TEXT,
    refund_reason           TEXT,
    refund_eligible			INT
    );
    """
)

conn.commit()

for order_id, order_data in orders.items():
    
    cursor.execute(
        """ 
        INSERT INTO orderss (
            order_id,
            customer_name,
            order_date,
            amount,
            payment_status,
            payment_method,
            payment_transaction_id,
            payment_error_code,
            shipping_status,
            tracking_number,
            estimated_delivery,
            delivery_date,
            refund_status,
            refund_reason,
            refund_eligible
        )
        VALUES(
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            order_id,
            order_data['customer_name'],
            order_data['order_date'],
            order_data['amount'],
            order_data['payment']['status'],
            order_data['payment']['method'],
            order_data['payment']['transaction_id'],
            order_data['payment']['error_code'],
            order_data['shipping']['order_status'],
            order_data['shipping']['tracking_number'],
            order_data['shipping']['estimated_delivery'],
            order_data['shipping']['delivery_date'],
            order_data['refund']['status'],
            order_data['refund']['reason'],
            order_data['refund']['eligible']
        )
    )
    
conn.commit()
conn.close()