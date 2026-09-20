import tkinter as tk
from tkinter import ttk, messagebox
from cafeku.database import connect_db
from datetime import datetime
import os


class PaymentPage:

    def __init__(
        self,
        root,
        transaksi_id,
        refresh_callback
    ):

        self.transaksi_id = transaksi_id
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(root)

        self.window.title(
            "CaféKu - Pembayaran"
        )

        self.window.geometry(
            "500x500"
        )

        self.load_transaction()
        self.create_widgets()

    def load_transaction(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                transaksi.*,
                meja.nomor_meja
            FROM transaksi
            JOIN meja
            ON transaksi.meja_id = meja.id
            WHERE transaksi.id=?
        """, (self.transaksi_id,))

        self.transaction = cursor.fetchone()

        conn.close()

    def create_widgets(self):

        tk.Label(
            self.window,
            text="💳 PEMBAYARAN",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            self.window,
            text=f"Transaksi: #{self.transaksi_id}",
            font=("Arial", 12)
        ).pack()

        tk.Label(
            self.window,
            text=f"Meja: {self.transaction['nomor_meja']}",
            font=("Arial", 12)
        ).pack(pady=5)

        tk.Label(
            self.window,
            text=f"Total: Rp {self.transaction['total']:,.0f}",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            self.window,
            text="Metode Pembayaran"
        ).pack()

        self.method = ttk.Combobox(
            self.window,
            values=[
                "Cash",
                "QRIS",
                "E-Wallet"
            ],
            state="readonly",
            width=25
        )

        self.method.current(0)

        self.method.pack(pady=10)

        tk.Label(
            self.window,
            text="Status Pembayaran"
        ).pack()

        self.status = ttk.Combobox(
            self.window,
            values=[
                "Berhasil",
                "Gagal",
                "Pending"
            ],
            state="readonly",
            width=25
        )

        self.status.current(0)

        self.status.pack(pady=10)

        tk.Button(
            self.window,
            text="PROSES PEMBAYARAN",
            command=self.process_payment,
            bg="#4caf50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=20)

    def process_payment(self):

        method = self.method.get()
        status = self.status.get()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE transaksi
            SET metode_pembayaran=?,
                status=?
            WHERE id=?
        """, (
            method,
            status if status != "Berhasil"
            else "Lunas",
            self.transaksi_id
        ))

        if status == "Berhasil":

            cursor.execute("""
                UPDATE meja
                SET status='Kosong'
                WHERE id = (
                    SELECT meja_id
                    FROM transaksi
                    WHERE id=?
                )
            """, (self.transaksi_id,))

        conn.commit()
        conn.close()

        if status == "Berhasil":

            self.create_receipt(
                method
            )

            messagebox.showinfo(
                "Pembayaran",
                "Pembayaran berhasil.\nStruk telah dibuat."
            )

        elif status == "Pending":

            messagebox.showinfo(
                "Pembayaran",
                "Pembayaran masih pending."
            )

        else:

            messagebox.showerror(
                "Pembayaran",
                "Pembayaran gagal."
            )

        self.refresh_callback()
        self.window.destroy()

    def create_receipt(self, method):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                transaksi.*,
                meja.nomor_meja
            FROM transaksi
            JOIN meja
            ON transaksi.meja_id = meja.id
            WHERE transaksi.id=?
        """, (self.transaksi_id,))

        transaksi = cursor.fetchone()

        cursor.execute("""
            SELECT
                detail_transaksi.*,
                menu.nama
            FROM detail_transaksi
            JOIN menu
            ON detail_transaksi.menu_id = menu.id
            WHERE transaksi_id=?
        """, (self.transaksi_id,))

        details = cursor.fetchall()

        conn.close()

        filename = os.path.join(
            "struk",
            f"struk_{self.transaksi_id}.txt"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("=" * 40 + "\n")
            file.write("             CAFÉKU\n")
            file.write("       Cafe Management System\n")
            file.write("=" * 40 + "\n")

            file.write(
                f"Transaksi : #{transaksi['id']}\n"
            )

            file.write(
                f"Tanggal   : {transaksi['tanggal']}\n"
            )

            file.write(
                f"Meja      : {transaksi['nomor_meja']}\n"
            )

            file.write("-" * 40 + "\n")

            for item in details:

                file.write(
                    f"{item['nama']}\n"
                )

                file.write(
                    f"  {item['jumlah']} x "
                    f"Rp {item['harga']:,.0f} = "
                    f"Rp {item['subtotal']:,.0f}\n"
                )

            file.write("-" * 40 + "\n")

            file.write(
                f"Diskon    : "
                f"Rp {transaksi['diskon']:,.0f}\n"
            )

            file.write(
                f"TOTAL     : "
                f"Rp {transaksi['total']:,.0f}\n"
            )

            file.write(
                f"Pembayaran: {method}\n"
            )

            file.write("=" * 40 + "\n")
            file.write("       Terima kasih!\n")
            file.write("=" * 40 + "\n")