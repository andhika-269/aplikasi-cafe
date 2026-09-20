import tkinter as tk
from tkinter import ttk, messagebox
from cafeku.database import connect_db


class WaiterPage:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title(
            "CaféKu - Dashboard Waiter"
        )

        self.window.geometry(
            "1000x600"
        )

        self.create_widgets()
        self.load_orders()

    def create_widgets(self):

        tk.Label(
            self.window,
            text="🍽 PESANAN MASUK",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        columns = (
            "id",
            "tanggal",
            "meja",
            "total",
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

        buttons = tk.Frame(
            self.window
        )

        buttons.pack(pady=10)

        tk.Button(
            buttons,
            text="Proses Pesanan",
            command=self.process_order,
            bg="#ff9800",
            fg="white",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Selesai Dilayani",
            command=self.finish_order,
            bg="#4caf50",
            fg="white",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Refresh",
            command=self.load_orders
        ).pack(side="left", padx=5)

    def load_orders(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                transaksi.id,
                transaksi.tanggal,
                meja.nomor_meja,
                transaksi.total,
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
                    row["status"]
                )
            )

    def get_selected_id(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Peringatan",
                "Pilih pesanan."
            )

            return None

        return self.tree.item(
            selected[0]
        )["values"][0]

    def update_status(self, status):

        transaksi_id = self.get_selected_id()

        if not transaksi_id:
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE transaksi
            SET status=?
            WHERE id=?
        """, (
            status,
            transaksi_id
        ))

        conn.commit()
        conn.close()

        self.load_orders()

    def process_order(self):

        self.update_status(
            "Diproses"
        )

    def finish_order(self):

        self.update_status(
            "Selesai Dilayani"
        )