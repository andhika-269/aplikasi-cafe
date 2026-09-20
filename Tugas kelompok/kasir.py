import tkinter as tk
from tkinter import ttk, messagebox
from cafeku.database import connect_db
from pembayaran import PaymentPage
from datetime import datetime


class KasirPage:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title(
            "CaféKu - Kasir"
        )

        self.window.geometry(
            "1000x600"
        )

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):

        top = tk.Frame(
            self.window,
            pady=10
        )

        top.pack(fill="x")

        tk.Label(
            top,
            text="Nomor Meja:"
        ).pack(side="left", padx=5)

        self.meja = tk.Entry(
            top,
            width=10
        )

        self.meja.pack(
            side="left"
        )

        tk.Button(
            top,
            text="Cari",
            command=self.load_transactions
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            top,
            text="Semua",
            command=self.load_all
        ).pack(
            side="left"
        )

        columns = (
            "id",
            "tanggal",
            "meja",
            "total",
            "metode",
            "status"
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.tree.heading(
                col,
                text=col.title()
            )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        bottom = tk.Frame(
            self.window
        )

        bottom.pack(pady=10)

        tk.Button(
            bottom,
            text="Bayar",
            command=self.open_payment,
            bg="#4caf50",
            fg="white",
            padx=20,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            bottom,
            text="Refresh",
            command=self.load_transactions
        ).pack(
            side="left",
            padx=5
        )

    def load_all(self):

        self.meja.delete(0, tk.END)

        self.load_transactions()

    def load_transactions(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        meja = self.meja.get().strip()

        if meja:

            cursor.execute("""
                SELECT
                    transaksi.id,
                    transaksi.tanggal,
                    meja.nomor_meja,
                    transaksi.total,
                    transaksi.metode_pembayaran,
                    transaksi.status
                FROM transaksi
                JOIN meja
                ON transaksi.meja_id = meja.id
                WHERE meja.nomor_meja=?
                AND transaksi.status != 'Lunas'
                ORDER BY transaksi.id DESC
            """, (meja,))

        else:

            cursor.execute("""
                SELECT
                    transaksi.id,
                    transaksi.tanggal,
                    meja.nomor_meja,
                    transaksi.total,
                    transaksi.metode_pembayaran,
                    transaksi.status
                FROM transaksi
                JOIN meja
                ON transaksi.meja_id = meja.id
                WHERE transaksi.status != 'Lunas'
                ORDER BY transaksi.id DESC
            """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["tanggal"],
                    row["nomor_meja"],
                    f"Rp {row['total']:,.0f}",
                    row["metode_pembayaran"] or "-",
                    row["status"]
                )
            )

    def open_payment(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Peringatan",
                "Pilih transaksi."
            )

            return

        transaksi_id = self.tree.item(
            selected[0]
        )["values"][0]

        PaymentPage(
            self.window,
            transaksi_id,
            self.load_transactions
        )