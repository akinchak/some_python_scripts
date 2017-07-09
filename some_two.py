import sqlite3
import csv

# open file
with open('feed.csv') as f:
    f_csv = csv.reader(f)
    header = next(f_csv)    
    rows = [row for row in f_csv]

rows = [word.rstrip() for row in rows for word in row]
head_len = len(header)
rows_len = len(rows)
new_rows = [rows[i:i+head_len] for i in range(0, rows_len, head_len)]


# retrieving data as list example:
'''
print(header)
for row in new_rows:    
    print(row)

input()
'''
# retrieving data as dict example:
'''
for row in new_rows:
     row = dict(zip(header, row))
     print(row)

input()
'''


# create sqlite mydb database record
'''
db = sqlite3.connect('mydb.db')
c = db.cursor()
c.execute('CREATE TABLE tbl (upc, name, sku, tax, price, color, size, onhand,\
           season, category_1, category_2, category_3, color_code, season_code,\
           description, sale_price, on_sale)')
db.commit()
c.executemany('INSERT INTO tbl VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', new_rows)
db.commit()
'''

# retrieving mydb data example:
'''
con = sqlite3.connect('mydb.db')
for row in con.execute('select upc, name, color from tbl'):    
    print(row)

input()
'''

# dump
'''
def dump_to_file(conn, filename='dump.sql'):    
    with open(filename, 'w') as f:
        for line in conn.iterdump():
            f.write('{}\n'.format(line))

conn = sqlite3.connect('mydb.db')

dump_to_file(conn)
'''

# restore from dump
'''
def restore_db(conn, db_file, filename='dump.sql'):    
    with open(filename, 'r') as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()
    
conn.close()

conn = sqlite3.connect('new_mydb.db')
restore_db(conn, db_file='new_mydb.db')
conn.close()
'''

# retrieving data example:
'''
con = sqlite3.connect('new_mydb.db')
for row in con.execute('select name, color, size from tbl'):    
    print(row)

input()
'''



# UPDATE VERSION SINCE 01/02/2017

# create sqlite mydb_main.db from mydb.db
db = sqlite3.connect('mydb.db')
c = db.cursor()
c.execute('CREATE TABLE tbl (upc, name, sku, tax, price, color, size, onhand,\
           season, category_1, category_2, category_3, color_code, season_code,\
           description, sale_price, on_sale)')
db.commit()
c.executemany('INSERT INTO tbl VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', new_rows)
db.commit()

con = sqlite3.connect('mydb.db')
main = [row for row in con.execute('select upc, sku, tax, price, size, onhand, season,\
                                    category_1, category_2, category_3, color_code, season_code,\
                                    description, sale_price, on_sale from tbl')]
color = [row for row in con.execute('select color, color_code from tbl')]
name = [row for row in con.execute('select name, sku from tbl')]
color = set(color)
name = set(name)


# mydb_main.db
db = sqlite3.connect('mydb_main.db')
c = db.cursor()
c.execute('CREATE TABLE tbl_name (name, sku_id PRIMARY KEY)')
c.execute('CREATE TABLE tbl_color (color, color_id PRIMARY KEY)')
c.execute('CREATE TABLE tbl_main (upc, sku, tax, price, size, onhand, season, category_1,\
                                  category_2, category_3, color_code, season_code, description,\
                                  sale_price, on_sale, FOREIGN KEY(sku) REFERENCES tbl_name(sku_id),\
                                  FOREIGN KEY(color_code) REFERENCES tbl_color(color_id))')

db.commit()

c.executemany('INSERT INTO tbl_name VALUES (?,?)', name)
c.executemany('INSERT INTO tbl_color VALUES (?,?)', color)
c.executemany('INSERT INTO tbl_main VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', main)
db.commit()
