import sqlite3 as sql;

conn = sql.connect(database="_employee.db")

c = conn.cursor()

c.execute("""CREATE TABLE employees (
    first text, 
    last text,
    pay integer
)""")

conn.commit()
conn.close()  