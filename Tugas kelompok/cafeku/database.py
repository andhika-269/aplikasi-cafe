import sqlite3
import os

# ==========================================
# KONFIGURASI
# ==========================================

DATABASE_FOLDER = "database"
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "cafeku.db")


# ==========================================
# MEMBUAT FOLDER
# ==========================================

os.makedirs(DATABASE_FOLDER, exist_ok=True)
os.makedirs("images/menu", exist_ok=True)
os.makedirs("struk", exist_ok=True)


# ==========================================
# KONEKSI DATABASE
# ==========================================

def connect_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# MEMBUAT TABEL
# ==========================================

def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    # USER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # MENU
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kategori TEXT NOT NULL,
            harga REAL NOT NULL,
            stok INTEGER DEFAULT 0,
            foto TEXT,
            status TEXT DEFAULT 'Tersedia'
        )
    """)

    # MEJA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomor_meja INTEGER UNIQUE NOT NULL,
            status TEXT DEFAULT 'Kosong'
        )
    """)

    # TRANSAKSI
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            user_id INTEGER,
            meja_id INTEGER,
            total REAL DEFAULT 0,
            diskon REAL DEFAULT 0,
            metode_pembayaran TEXT,
            status TEXT DEFAULT 'Menunggu',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (meja_id) REFERENCES meja(id)
        )
    """)

    # DETAIL TRANSAKSI
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaksi_id INTEGER NOT NULL,
            menu_id INTEGER NOT NULL,
            jumlah INTEGER NOT NULL,
            harga REAL NOT NULL,
            subtotal REAL NOT NULL,
            diskon REAL DEFAULT 0,
            FOREIGN KEY (transaksi_id) REFERENCES transaksi(id),
            FOREIGN KEY (menu_id) REFERENCES menu(id)
        )
    """)

    # BAHAN
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bahan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_bahan TEXT NOT NULL,
            stok REAL DEFAULT 0,
            satuan TEXT NOT NULL
        )
    """)

    # PROMO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT UNIQUE NOT NULL,
            nama TEXT NOT NULL,
            diskon REAL NOT NULL,
            status TEXT DEFAULT 'Aktif'
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# USER DEFAULT
# ==========================================

def create_default_users():

    conn = connect_db()
    cursor = conn.cursor()

    users = [
        ("admin", "admin123", "Admin"),
        ("kasir", "kasir123", "Kasir"),
        ("waiter", "waiter123", "Waiter"),
        ("pembeli", "pembeli123", "Pembeli"),
        ("pemilik", "pemilik123", "Pemilik")
    ]

    for username, password, role in users:

        cursor.execute("""
            INSERT OR IGNORE INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))

    conn.commit()
    conn.close()


# ==========================================
# MEJA DEFAULT
# ==========================================

def create_default_tables():

    conn = connect_db()
    cursor = conn.cursor()

    for nomor in range(1, 11):

        cursor.execute("""
            INSERT OR IGNORE INTO meja
            (nomor_meja, status)
            VALUES (?, 'Kosong')
        """, (nomor,))

    conn.commit()
    conn.close()


# ==========================================
# MENU DEFAULT
# ==========================================

def create_default_menu():

    conn = connect_db()
    cursor = conn.cursor()

    menus = [
        ("Nasi Goreng", "Makanan", 20000, 20),
        ("Mie Goreng", "Makanan", 18000, 20),
        ("Chicken Steak", "Makanan", 25000, 15),
        ("Kentang Goreng", "Snack", 15000, 20),
        ("Roti Bakar", "Snack", 12000, 20),
        ("Es Teh", "Minuman", 5000, 30),
        ("Es Jeruk", "Minuman", 7000, 30),
        ("Kopi Susu", "Minuman", 15000, 25),
        ("Cappuccino", "Minuman", 18000, 25),
        ("Chocolate", "Minuman", 16000, 20)
    ]

    for nama, kategori, harga, stok in menus:

        cursor.execute("""
            SELECT id FROM menu
            WHERE nama = ?
        """, (nama,))

        if cursor.fetchone() is None:

            cursor.execute("""
                INSERT INTO menu
                (nama, kategori, harga, stok, status)
                VALUES (?, ?, ?, ?, 'Tersedia')
            """, (nama, kategori, harga, stok))

    conn.commit()
    conn.close()


# ==========================================
# PROMO DEFAULT
# ==========================================

def create_default_promos():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO promo
        (kode, nama, diskon, status)
        VALUES (?, ?, ?, ?)
    """, ("CAFE10", "Diskon 10%", 10, "Aktif"))

    conn.commit()
    conn.close()


# ==========================================
# INITIALIZE
# ==========================================

def initialize_database():

    create_tables()
    create_default_users()
    create_default_tables()
    create_default_menu()
    create_default_promos()

    print("Database CaféKu berhasil disiapkan.")


if __name__ == "__main__":
    initialize_database()