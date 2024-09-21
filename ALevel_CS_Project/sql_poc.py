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
# cur.execute("SELECT rowid, * FROM customers")

# items = cur.fetchall()

# for item in items:
#     print(item)

# Updating Records

# cur.execute("""UPDATE customers SET first_name = 'Bob'
#                 WHERE last_name = 'Elder'
# """)
# items = cur.fetchall()
#
# for item in items:
#     print(item)

# Deleting Records
cur.execute("DELETE FROM customers WHERE rowid = 4")

# Ordering Results

cur.execute("SELECT * FROM customers ORDER BY first_name")

# Using AND/OR
cur.execute("SELECT * FROM customers WHERE first_name = 'Bob' AND last_name = 'Elder'")
cur.execute("SELECT * FROM customers WHERE first_name = 'Wes' OR last_name = 'Elder'")

# Limit Results
cur.execute("SELECT * FROM customers LIMIT 2")

# Dropping Tables
# cur.execute("DROP TABLE customers")

conn.commit()

conn.close()
