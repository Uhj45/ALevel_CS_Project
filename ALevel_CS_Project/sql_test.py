import sqlite3

conn = sqlite3.connect('sqlite/customer.db')

cur = conn.cursor()

# Creates table

cur.execute("""CREATE TABLE customers(
first_name text,
last_name text,
email text
)""")

# Adding a single item to the table
cur.execute("INSERT INTO customers VALUES ('John', 'Elder', 'john@compnay.com')")



conn.commit()

conn.close()
