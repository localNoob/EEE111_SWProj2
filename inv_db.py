import sqlite3
import csv

def makeTable():
  link = sqlite3.connect('shop_inventory.db')
  c = link.cursor()

  c.execute('''
        CREATE TABLE IF NOT EXISTS shop_inventory (
            item_id TEXT PRIMARY KEY,
            name TEXT,
            desc TEXT,
            var TEXT,
            price REAL,
            qty INTEGER,
            inv_value REAL,
            cat TEXT,
            cont TEXT)''')
  link.commit()
  link.close()

def fetch_items():
  link = sqlite3.connect('shop_inventory.db')
  c = link.cursor()
  c.execute('SELECT * FROM shop_inventory')
  items = c.fetchall()
  link.close()
  return items

def add_item(item_id,name,desc,var,price,qty,cat,cont):
  link = sqlite3.connect('shop_inventory.db')
  inv_value = float(price*qty)
  inv_value = "{:.3f}".format(inv_value)
  c = link.cursor()
  c.execute('INSERT INTO shop_inventory (item_id, name, desc, var, price, qty, inv_value, cat, cont) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (item_id, name, desc, var, price, qty, inv_value, cat, cont))
  link.commit()
  link.close()

def delete_item(item_id):
  link = sqlite3.connect('shop_inventory.db')
  c = link.cursor()
  c.execute('DELETE FROM shop_inventory WHERE item_id = ?', (item_id,))
  link.commit()
  link.close()

def update_item(name_new, desc_new, var_new, price_new, qty_new, new_cat, new_cont, item_id):
  link = sqlite3.connect('shop_inventory.db')
  c = link.cursor()
  new_inv = float(price_new*qty_new)
  new_inv = "{:.3f}".format(new_inv)
  c.execute('UPDATE shop_inventory SET name = ?, desc = ?, var = ?, price = ?, qty = ?, inv_value = ?, cat = ?, cont = ? WHERE item_id  = ?', (name_new, desc_new, var_new, price_new, qty_new, new_inv, new_cat, new_cont, item_id))
  link.commit()
  link.close()

def same_id(item_id):
  link = sqlite3.connect('shop_inventory.db')
  c = link.cursor()
  c.execute('SELECT COUNT(*) FROM shop_inventory WHERE item_id = ?', (item_id,))
  found = c.fetchone()
  link.commit()
  link.close()
  return found[0] > 0

def exportCSV():
  with open('shop_inventory.csv', 'w') as handle:
    dbItems = fetch_items()
    for item in dbItems:
      print(item)
      contents = f"{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]},{item[6]},{item[7]},{item[8]}\n"
      handle.write(contents)

def importCSV(file):
  link = sqlite3.connect('shop_inventory.db')
  c = link.cursor()
  c.execute('''
        CREATE TABLE IF NOT EXISTS shop_inventory (
            item_id TEXT PRIMARY KEY,
            name TEXT,
            desc TEXT,
            var TEXT,
            price REAL,
            qty INTEGER,
            inv_value REAL,
            cat TEXT,
            cont TEXT)''')
  contents = csv.reader(file)
  for data in contents:
    c.execute('INSERT INTO shop_inventory (item_id, name, desc, var, price, qty, inv_value, cat, cont) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',data)
  c.execute('SELECT * FROM shop_inventory').fetchall()
  link.commit()
  link.close()

makeTable()