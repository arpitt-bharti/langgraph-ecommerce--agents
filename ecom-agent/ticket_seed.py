import json, sqlite3

def create_ticket_table() : 
    
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' 
        create table if not exists tickets (
            ticket_id       TEXT        PRIMARY KEY,
            order_id        TEXT,
            description     TEXT,
            status          TEXT,
            created_date    DATE
        );
        '''
    )
    conn.commit()

if __name__ == '__main__' :
    create_ticket_table()
    print('ticket table created !')    
    
    
