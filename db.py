import sqlite3

def init_db():
    conn = sqlite3.connect('vm_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vms (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL,
            ip TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_vm(name, status, date, ip):
    conn = sqlite3.connect('vm_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO vms (name, status, date, ip) VALUES (?, ?, ?, ?)', (name, status, date, ip))
    conn.commit()
    conn.close()

def get_vms():
    conn = sqlite3.connect('vm_data.db')
    c = conn.cursor()
    c.execute('SELECT name, status, date, ip FROM vms')
    vms = c.fetchall()
    conn.close()
    return vms
