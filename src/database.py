#py-stock
#Valver-Dev - Manu Valverde
#December 2021

import sqlite3
from typing import List
from model import Item

conn = sqlite3.connect('stock.db')
c = conn.cursor()


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        category TEXT,
        uds INTEGER
    )""")


create_table()


def insert_item(item: Item):
   c.execute("SELECT COUNT(*) FROM stock WHERE item = ?",(item.name,))
   count = c.fetchone()[0]
   if count == 0:
       with conn:
           c.execute('INSERT INTO stock (item, category, uds) VALUES(:item, :category, :uds)',
           {'id': item.id, 'item': item.name, 'category': item.category, 'uds': item.uds})


def get_stock() -> List[Item]:
    c.execute('SELECT * FROM stock')
    results = c.fetchall()
    stock = []
    for result in results:
        stock.append(Item(*result))
    return stock


def get_filtered_stock(filter: str, item: Item) -> List[Item]:
    stock = []
    if filter == 'id':
        crit = item.id
    elif filter == 'item':
        crit = item.name
    elif filter == 'category':
        crit = item.category
    else:
        return stock
    
    c.execute(f"SELECT * FROM stock WHERE {filter} = ?",(crit,))
    results = c.fetchall()
    for result in results:
        stock.append(Item(*result))
    return stock


def update_item(id: int, category: str, uds: int):
    c.execute("SELECT uds FROM stock WHERE id = ?",(id,))
    uds_prev = c.fetchone()[0]
    with conn:        
        if category is not None and uds is None:
            c.execute('UPDATE stock SET category = :category WHERE id = :id',
            {'id': id, 'category': category})
        else:
            if (uds_prev + uds) >= 0: 
                c.execute('UPDATE stock SET uds = :uds WHERE id = :id',
                {'id': id, 'uds': uds_prev + uds})

def delete_item(id: int):
    c.execute('DELETE FROM stock WHERE id = :id',{'id': id,})
    conn.commit()