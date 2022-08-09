import psycopg2

# Функция создание таблиц
def create_db(cur):
    cur.execute("""
    DROP TABLE IF EXISTS phones;""")
    cur.execute("""
    DROP TABLE IF EXISTS clients;""")
    cur.execute("""
    CREATE TABLE Clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    surname VARCHAR(80) NOT NULL,
    email VARCHAR(80) NOT NULL
    );""")
    cur.execute("""
    CREATE TABLE Phones (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES Clients(id),
    phone_number INTEGER NOT NULL
    );""")

# Функция, позволяющая добавить нового клиента
def add_client(cursor, name, surname, email):
    cursor.execute("""
    INSERT INTO clients(name, surname, email)
    VALUES(%s, %s, %s);
    """, (name, surname, email))

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(cursor, client_id, phone_number):
    cursor.execute("""
    INSERT INTO phones(client_id, phone_number) VALUES(%s, %s);
    """, (client_id, phone_number))

# Функция, позволяющая изменить данные о клиенте
def change_client(cursor, conn, client_id, name=None, surname=None, email=None):
    if name != None:
        cursor.execute("""
        UPDATE clients SET name=%s WHERE id=%s;
        """, (name, client_id))
    if surname != None:
        cursor.execute("""
        UPDATE clients SET surname=%s WHERE id=%s;
        """, (surname, client_id))
    if email != None:
        cursor.execute("""
        UPDATE clients SET email=%s WHERE id=%s;
        """, (email, client_id))
    conn.commit()

# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(cursor, conn, client_id, phone):
    cursor.execute("""
    DELETE FROM phones WHERE client_id=%s AND phone_number=%s;
    """, (client_id, phone))
    conn.commit()

#Функция, позволяющая удалить существующего клиента
def delete_client(cursor, conn, client_id):
    cur.execute("""
    DELETE FROM phones p WHERE p.client_id=%s;
    """, (client_id,))
    cur.execute("""
    DELETE FROM clients c WHERE c.id=%s;
    """, (client_id,))
    conn.commit()

#Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(cursor, id=None, name=None, surname=None, email=None):
    cursor.execute("""
    SELECT name FROM clients c
    WHERE c.id=%s OR c.name=%s OR c.surname=%s OR c.email=%s
    """, (id, name, surname, email))
    print(cur.fetchall())

def print_all_clients(cursor):
    cur.execute("""
    SELECT * FROM clients;
    """)
    print(cur.fetchall())

def print_all_phones(cursor):
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())

with psycopg2.connect(database="clients_db", user="postgres", password="111395") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, 'Петя', 'Иванов', 'ввв@ddd.ru')
        add_client(cur, 'Вася', 'Петров', 'ууу@ллл.ru')
        add_phone(cur, 1, 12458695)
        add_phone(cur, 1, 321654)
        add_phone(cur, 1, 4585695)

        conn.commit()

        find_client(cur, 1)

        change_client(cur, conn, 1, name='Вова', email='111@111.ru')

        find_client(cur, 1)

        print_all_phones(cur)

        delete_phone(cur, conn, 1, 12458695)

        print_all_phones(cur)

        print_all_clients(cur)

        delete_client(cur, conn, 1)

        print_all_clients(cur)

conn.close()
