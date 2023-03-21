import psycopg2


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
