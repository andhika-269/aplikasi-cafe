import tkinter as tk
from tkinter import ttk, messagebox
from cafeku.database import connect_db
from datetime import datetime


class OrderPage:

    def __init__(self, root, user):

        self.user = user
        self.window = tk.Toplevel(root)

        self.window.title("CaféKu - Pemesanan")
        self.window.geometry("1000x650")

        self.cart = []

        self.create_widgets()
        self.load_menu()
        self.load_tables()

    def create_widgets(self):

        top = tk.Frame(
            self.window,
            padx=15,
            pady=10
        )

        top.pack(fill="x")

        tk.Label(
            top,
            text="Nomor Meja:"
        ).pack(side="left")

        self.table_combo = ttk.Combobox(
            top,
            state="readonly",
            width=15
        )

        self.table_combo.pack(
            side="left",
            padx=10
        )

        tk.Label(
            top,
            text="Kode Promo:"
        ).pack(side="left")

        self.promo = tk.Entry(
            top,
            width=15
        )

        self.promo.pack(
            side="left",
            padx=10
        )

        # MENU
        menu_frame = tk.LabelFrame(
            self.window,
            text="Daftar Menu"
        )

        menu_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "id",
            "nama",
            "kategori",
            "harga",
            "stok"
        )

        self.menu_tree = ttk.Treeview(
            menu_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.menu_tree.heading(
                col,
                text=col.title()
            )

        self.menu_tree.pack(
            fill="both",
            expand=True
        )

        add_frame = tk.Frame(
            menu_frame
        )

        add_frame.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            add_frame,
            text="Jumlah:"
        ).pack(side="left")

        self.jumlah = tk.Spinbox(
            add_frame,
            from_=1,
            to=99,
            width=5
        )

        self.jumlah.pack(
            side="left",
            padx=5
        )

        tk.Button(
            add_frame,
            text="Tambah ke Pesanan",
            command=self.add_cart,
            bg="#6f4e37",
            fg="white"
        ).pack(
            side="left",
            padx=10
        )

        # CART
        cart_frame = tk.LabelFrame(
            self.window,
            text="Pesanan Saya"
        )

        cart_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.cart_tree = ttk.Treeview(
            cart_frame,
            columns=(
                "nama",
                "jumlah",
                "harga",
                "subtotal"
            ),
            show="headings"
        )

        for col in (
            "nama",
            "jumlah",
            "harga",
            "subtotal"
        ):

            self.cart_tree.heading(
                col,
                text=col.title()
            )

        self.cart_tree.pack(
            fill="both",
            expand=True
        )

        tk.Button(
            cart_frame,
            text="Hapus Item",
            command=self.remove_cart
        ).pack(pady=5)

        self.total_label = tk.Label(
            cart_frame,
            text="Total: Rp 0",
            font=("Arial", 16, "bold")
        )

        self.total_label.pack(
            pady=10
        )

        tk.Button(
            cart_frame,
            text="PESAN SEKARANG",
            command=self.checkout,
            bg="#4caf50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        ).pack()

    def load_tables(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nomor_meja
            FROM meja
            WHERE status='Kosong'
        """)

        tables = [
            str(row["nomor_meja"])
            for row in cursor.fetchall()
        ]

        conn.close()

        self.table_combo["values"] = tables

        if tables:
            self.table_combo.current(0)

    def load_menu(self):

        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nama, kategori, harga, stok
            FROM menu
            WHERE status='Tersedia'
            AND stok > 0
            ORDER BY kategori, nama
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            self.menu_tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["nama"],
                    row["kategori"],
                    row["harga"],
                    row["stok"]
                )
            )

    def add_cart(self):

        selected = self.menu_tree.selection()

        if not selected:

            messagebox.showwarning(
                "Peringatan",
                "Pilih menu terlebih dahulu."
            )

            return

        values = self.menu_tree.item(
            selected[0]
        )["values"]

        menu_id = values[0]
        nama = values[1]
        harga = float(values[3])
        stok = int(values[4])

        jumlah = int(self.jumlah.get())

        if jumlah > stok:

            messagebox.showwarning(
                "Stok",
                "Jumlah melebihi stok."
            )

            return

        for item in self.cart:

            if item["menu_id"] == menu_id:

                if item["jumlah"] + jumlah > stok:

                    messagebox.showwarning(
                        "Stok",
                        "Jumlah pesanan melebihi stok."
                    )

                    return

                item["jumlah"] += jumlah

                self.refresh_cart()

                return

        self.cart.append({
            "menu_id": menu_id,
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah
        })

        self.refresh_cart()

    def refresh_cart(self):

        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        total = 0

        for item in self.cart:

            subtotal = (
                item["harga"] *
                item["jumlah"]
            )

            total += subtotal

            self.cart_tree.insert(
                "",
                "end",
                values=(
                    item["nama"],
                    item["jumlah"],
                    f"Rp {item['harga']:,.0f}",
                    f"Rp {subtotal:,.0f}"
                )
            )

        self.total_label.config(
            text=f"Total: Rp {total:,.0f}"
        )

    def remove_cart(self):

        selected = self.cart_tree.selection()

        if not selected:
            return

        index = self.cart_tree.index(
            selected[0]
        )

        del self.cart[index]

        self.refresh_cart()

    def checkout(self):

        if not self.cart:

            messagebox.showwarning(
                "Pesanan",
                "Belum ada menu yang dipesan."
            )

            return

        if not self.table_combo.get():

            messagebox.showwarning(
                "Meja",
                "Pilih nomor meja."
            )

            return

        subtotal = sum(
            item["harga"] * item["jumlah"]
            for item in self.cart
        )

        diskon = 0

        kode = self.promo.get().strip().upper()

        if kode:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT diskon
                FROM promo
                WHERE kode=?
                AND status='Aktif'
            """, (kode,))

            promo = cursor.fetchone()

            conn.close()

            if promo:

                diskon = (
                    subtotal *
                    promo["diskon"] /
                    100
                )

            else:

                messagebox.showwarning(
                    "Promo",
                    "Kode promo tidak valid."
                )

                return

        total = subtotal - diskon

        table_number = int(
            self.table_combo.get()
        )

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM meja
            WHERE nomor_meja=?
        """, (table_number,))

        meja = cursor.fetchone()

        if not meja:

            conn.close()

            messagebox.showerror(
                "Error",
                "Meja tidak ditemukan."
            )

            return

        tanggal = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO transaksi
            (tanggal, user_id, meja_id, total, diskon, status)
            VALUES (?, ?, ?, ?, ?, 'Menunggu')
        """, (
            tanggal,
            self.user["id"],
            meja["id"],
            total,
            diskon
        ))

        transaksi_id = cursor.lastrowid

        for item in self.cart:

            subtotal_item = (
                item["harga"] *
                item["jumlah"]
            )

            cursor.execute("""
                INSERT INTO detail_transaksi
                (transaksi_id, menu_id, jumlah, harga, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (
                transaksi_id,
                item["menu_id"],
                item["jumlah"],
                item["harga"],
                subtotal_item
            ))

            cursor.execute("""
                UPDATE menu
                SET stok = stok - ?
                WHERE id = ?
            """, (
                item["jumlah"],
                item["menu_id"]
            ))

        cursor.execute("""
            UPDATE menu
            SET status =
                CASE
                    WHEN stok <= 0 THEN 'Habis'
                    ELSE 'Tersedia'
                END
        """)

        cursor.execute("""
            UPDATE meja
            SET status='Terisi'
            WHERE id=?
        """, (meja["id"],))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Pesanan Berhasil",
            f"Pesanan berhasil dibuat!\n\n"
            f"Nomor transaksi: {transaksi_id}\n"
            f"Meja: {table_number}\n"
            f"Total: Rp {total:,.0f}"
        )

        self.cart.clear()
        self.refresh_cart()
        self.load_menu()
        self.load_tables()