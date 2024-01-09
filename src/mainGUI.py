from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from ttkthemes import ThemedTk #if underlined, fix it by changing interpreter to latest python version
import inv_db

app = ThemedTk(theme='adapta')
app.title('Electronics Shop Inventory')
app.geometry('1240x690')
app.resizable(False, False)

db = inv_db

#button functionalities
def add_to_table():
  items = inv_db.fetch_items()
  table.delete(*table.get_children())
  for item in items:
    table.insert('', END, values=item)

def clear_fields(*clicked):
    if clicked:
      table.selection_remove(table.focus())
      table.focus('')
    itemID.delete(0, END)
    nameEntry.delete(0, END)
    description.delete('1.0', END)
    variation.delete(0, END)
    unitPrice.delete(0, END)
    qtyStock.delete(0, END)
    category.set('Components')
    continuity.set('No')

def add_new_item():
  item_id = itemID.get()
  name = nameEntry.get()
  desc = description.get('1.0', 'end-1c')
  var = variation.get()
  price = unitPrice.get()
  qty = qtyStock.get()
  kind = category.get()
  cont = continuity.get()
  blank = item_id == '' or name == '' or desc == '' or var == '' or price == ''\
  or qty == '' or kind == '' or cont == ''

  if not (item_id and name and desc and var and price and qty and kind and cont):
    messagebox.showerror('Error', "Incomplete entries.")
  elif inv_db.same_id(item_id):
    messagebox.showerror('Error', "Item's ID must be unique!")
  elif blank:
    messagebox.showerror('Error', "No fields can be left blank.")
  else:
    inv_db.add_item(item_id, name, desc.replace(',',';'), var, float(price), int(qty), kind, cont)
    add_to_table()
    clear_fields()
    messagebox.showinfo('Success', 'Item added.')
  
def delete_selected():
  toDelete = table.focus()
  if not toDelete:
    messagebox.showerror('Error', 'Choose an item to delete.')
  else:
    item_id = itemID.get()
    inv_db.delete_item(item_id)
    add_to_table()
    clear_fields()
    messagebox.showinfo('Success', 'Item deleted.')

def update_selected():
  toUpdate = table.focus()
  if not toUpdate:
    messagebox.showerror('Error', 'Choose an item to update.')
  else:
    item_id = itemID.get()
    name = nameEntry.get()
    desc = description.get('1.0', 'end-1c')
    var = variation.get()
    price = unitPrice.get()
    qty = qtyStock.get()
    kind = category.get()
    cont = continuity.get()
    inv_db.update_item(name, desc.replace(',',';'), var, float(price), int(qty), kind, cont, item_id)
    add_to_table()
    clear_fields()
    messagebox.showinfo('Success', 'Item updated.')

def read_display(event):
  toRead = table.focus()
  if toRead:
    row = table.item(toRead)['values']
    clear_fields()
    itemID.insert(0, row[0])
    nameEntry.insert(0, row[1])
    description.insert(END, row[2])
    variation.insert(0, row[3])
    unitPrice.insert(0, row[4])
    qtyStock.insert(0, row[5])
    category.set(row[7])
    continuity.set(row[8])
  else: pass

#exporting to csv
def toCSV():
  db.exportCSV()
  messagebox.showinfo('Success', 'Data exported to shop_inventory.csv')

#importing from csv files
def fromCSV():
  filepath = filedialog.askopenfile(title='CSV file to import',filetypes=[('CSV Files','.csv')])
  db.importCSV(filepath)
  add_to_table()

#creating the tabular view
table = ttk.Treeview(app, height=16)
table['columns'] = ('Item ID', 'Name', 'Description', 'Variation', 'Unit Price', 'Qty. in Stock', 'Inventory Value', 'Category', 'Discontinued')
table.column('#0', width=0, stretch=NO)
table.column('Item ID', anchor=CENTER, width=100)
table.column('Name', anchor=CENTER, width=100)
table.column('Description', anchor=CENTER, width=200)
table.column('Variation', anchor=CENTER, width=100)
table.column('Unit Price', anchor=CENTER, width=100)
table.column('Qty. in Stock', anchor=CENTER, width=100)
table.column('Inventory Value', anchor=CENTER, width=200)
table.column('Category', anchor=CENTER, width=150)
table.column('Discontinued', anchor=CENTER, width=150)

table.heading('#0', text='', anchor=CENTER)
table.heading('Item ID', text='Item ID', anchor=CENTER)
table.heading('Name', text='Name', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Variation', text='Variation', anchor=CENTER)
table.heading('Unit Price', text='Unit Price', anchor=CENTER)
table.heading('Qty. in Stock', text='Qty. in Stock', anchor=CENTER)
table.heading('Inventory Value', text='Inventory Value', anchor=CENTER)
table.heading('Category', text='Category', anchor=CENTER)
table.heading('Discontinued', text='Discontinued', anchor=CENTER)

table['show'] = 'headings'
table.grid(row=0, column=0, columnspan=5)

#columns 0 and 1
itemLabel = Label(app, text='Item ID:')
itemLabel.grid(row=1, column=0, padx=(10,0))
itemID = Entry(app, width=40)
itemID.grid(row=1, column=1, padx=(0,10), ipady=5)

nameLabel = Label(app, text='Name:')
nameLabel.grid(row=2, column=0, padx=(10,0))
nameEntry = Entry(app, width=40)
nameEntry.grid(row=2, column=1, padx=(0,10), ipady=5)

descLabel = Label(app, text='Description:')
descLabel.grid(row=3, column=0, padx=(10,0))
description = Text(app, height=2, width=30)
description.grid(row=3, column=1, padx=(0,10), ipady=5)

varLabel = Label(app, text='Variation:')
varLabel.grid(row=4, column=0, padx=(10,0))
variation = Entry(app, width=40)
variation.grid(row=4, column=1, padx=(0,10), ipady=5)

#special row 5
clearAll = Button(app, text='Clear All', padx=50, pady=10, \
                  bg='lightsteelblue', fg='black', command=clear_fields)
clearAll.grid(row=5, column=0, columnspan=2)
importCSV = Button(app, text='Import from CSV', padx=40, pady=10, \
                  bg='dark orange', fg='black', command=fromCSV)
importCSV.grid(row=5, column=2, columnspan=2)

#columns 2 and 3
priceLabel = Label(app, text='Unit Price:')
priceLabel.grid(row=1, column=2, padx=10)
unitPrice= Entry(app, width=40)
unitPrice.grid(row=1, column=3, padx=10, ipady=5)

qtyLabel = Label(app, text='Qty. in Stock:')
qtyLabel.grid(row=2, column=2, padx=10)
qtyStock= Entry(app, width=40)
qtyStock.grid(row=2, column=3, padx=10, ipady=5)

categoryLabel = Label(app, text='Category:')
categoryLabel.grid(row=3, column=2, padx=10)
categoryOptions = ['Audio', 'Brands', 'Components', 'Custom', 'Development Tools',\
                   'E-Textiles', 'Miscellaneous', 'Robotics', 'Sensors', 'Tools', 'Wireless and IoT']
category = ttk.Combobox(app, values=categoryOptions, width=40)
category.current(2)
category.grid(row=3, column=3, padx=10)

contLabel = Label(app, text='Discontinued?')
contLabel.grid(row=4, column=2, padx=10)
contOptions = ['Yes', 'No']
continuity = ttk.Combobox(app, values=contOptions, width=40)
continuity.current(1)
continuity.grid(row=4, column=3, padx=10)

#columns 4 (buttons)
addItem = Button(app, text='Add Item', padx=30, pady=10, \
                 bg='limegreen', fg='black', command=add_new_item)
addItem.grid(row=1, column=4, padx=10, pady=(10,10))

deleteItem = Button(app, text='Delete Item', padx=30, pady=10, \
                    bg='tomato', fg='white', command=delete_selected)
deleteItem.grid(row=2, column=4, padx=10, pady=(0, 10))

updateItem = Button(app, text='Update Item', padx=30, pady=10, \
                    bg='yellow', fg='black', command=update_selected)
updateItem.grid(row=3, column=4, padx=10, pady=(0, 10))

exportCSV = Button(app, text='Export to CSV', padx=30, pady=10, \
                   bg='deepskyblue', fg='black', command=toCSV)
exportCSV.grid(row=4, column=4, padx=10, pady=(0,10))

table.bind('<ButtonRelease>', read_display)
add_to_table()
app.mainloop()