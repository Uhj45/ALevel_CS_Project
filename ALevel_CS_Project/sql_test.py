import sqlite3

conn = sqlite3.connect('sqlite/customer.db')

cur = conn.cursor()

# Creates table


conn.commit()

conn.close()
