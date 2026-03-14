import sqlite3

DB_NAME = 'kutubxona.db'

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def bazani_sozlash():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Kitoblar jadvali
        cursor.execute('''CREATE TABLE IF NOT EXISTS kitoblar 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           nomi TEXT, muallif TEXT, pdf_path TEXT)''')
        
        # FOYDALANUVCHILAR JADVALI (Yangi)
        cursor.execute('''CREATE TABLE IF NOT EXISTS foydalanuvchilar 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           username TEXT UNIQUE, password TEXT)''')
        conn.commit()

# Foydalanuvchini ro'yxatdan o'tkazish
def foydalanuvchi_qoshish(username, password):
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO foydalanuvchilar (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

# Foydalanuvchini tekshirish
def login_qilish(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM foydalanuvchilar WHERE username=? AND password=?", (username, password))
        return cursor.fetchone()

# (Qolgan eski funksiyalar: kitob_tahrirlash, kitob_ochirish o'z joyida qoladi)
def kitob_tahrirlash(id, nomi, muallif):
    with get_connection() as conn:
        conn.execute("UPDATE kitoblar SET nomi=?, muallif=? WHERE id=?", (nomi, muallif, id))
        conn.commit()

def kitob_ochirish(id):
    with get_connection() as conn:
        conn.execute("DELETE FROM kitoblar WHERE id=?", (id,))
        conn.commit()