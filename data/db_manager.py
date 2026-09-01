import psycopg2
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

def get_connect():
    return psycopg2.connect(
        dbname=DB_NAME,   # كان مكتوب db بدال dbname
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def create_tables():
    conn = get_connect()
    cur = conn.cursor()

    # جدول المستخدمين
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE,
            first_name VARCHAR(100),
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
     #|
    # جدول التصنيفات
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE 
        );
    ''')

    # جدول الكتب
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200),
            author VARCHAR(100),
            description TEXT,
            cover_path TEXT,
            file_path TEXT,
            category_id INT REFERENCES categories(id) ON DELETE CASCADE,
            added_by BIGINT REFERENCES users(telegram_id) ON DELETE SET NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ); 
    ''')

    conn.commit()
    cur.close()
    conn.close()

def add_category(name):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING",
        (name,)
    )
    conn.commit()  # نسيت ()
    cur.close()
    conn.close()
def get_books_by_category(category_id):
    conn = get_connect()   # كان غلط
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, author, description, cover_path, file_path
        FROM books
        WHERE category_id = %s
    """, (category_id,))
    rows = cur.fetchall() #هنا يوجد خطأ بالغالب بحكم انه المفروض نضيف علاقة بحيث الكتاب الملف يكونى مربوط بالجدول الاول ثم جدول books
    cur.close()
    conn.close()
    return rows



def add_book(title, author, description, cover_path, file_path, category_id, added_by):
    conn = get_connect()   # كان غلط
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO books (title, author, description, cover_path, file_path, category_id, added_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)  
    """, (title, author, description, cover_path, file_path, category_id, added_by))#%s لمنع حقن sql 
    conn.commit()
    cur.close()
    conn.close()

def get_categories():
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM categories")  # جلب جميع الفئات
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows #يرجع لك كل التصنيفات 