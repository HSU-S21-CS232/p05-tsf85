import sqlite3

def run_query(sql, params = ()):

    #grab data from DB
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sql, params) 
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def run_total(sql, params = ()):

    #grab data from DB
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sql, params) 
    result = cursor.fetchone() [0]
    cursor.close()
    db.close()
    return result

def run_insert(sql, params):
    #grab data from DB
    db = sqlite3.connect('chinook.db')
    cursor = db.cursor()
    cursor.execute(sql, params)
    id = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return id

def run_delete(sql, params):
    #grab data from DB
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sql, params)
    id = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return id

def run_clear(sql):
    #grab data from DB
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sql)
    id = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return id

