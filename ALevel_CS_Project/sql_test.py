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
# cur.execute("INSERT INTO customers VALUES ('John', 'Elder', 'john@compnay.com')")

# Adding multiple items to a table
# many_customers = [
#     ('Wes', 'Brown', 'wes@brown.com'),
#     ('Steph', 'Kuewa', 'steph@kuewa.com'),
#     ('Dan', 'Pas', 'dan@pas.com'),
# ]
#
# cur.executemany("INSERT INTO customers VALUES (?,?,?)", many_customers)

# Printing Table with a primary key in python console
cur.execute("SELECT rowid, * FROM customers")

items = cur.fetchall()

for item in items:
    print(item)



conn.commit()

conn.close()
