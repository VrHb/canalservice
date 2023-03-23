import psycopg2



def create_table(user, password, host, port, dbname, table_name):
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password, 
        port=port
    )
    cursor = conn.cursor()
    cursor.execute(
        f"""
        create table if not exists {table_name} 
        (
        id integer primary key,
        order_id integer,
        usd_price integer,
        rub_price integer,
        delivery_time date,
        unique(order_id)
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()
    

def request_to_db(user, password, host, port, dbname, query):
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password, 
        port=port
    )
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
