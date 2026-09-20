import tkinter as tk
from tkinter import ttk
from cafeku.database import connect_db
from datetime import datetime
import matplotlib.pyplot as plt

class LaporanPage:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title(
            "CaféKu - Laporan Penjualan"
        )

        self.window.geometry(
            "1000x650"
        )

        self.create_widgets()
        self.load_report()

    def create_widgets(self):

        top = tk.Frame(
            self.window,
            pady=10
        )

        top.pack(fill="x")

        tk.Label(
            top,
            text="Periode:"
        ).pack(side="left", padx=5)

        self.period = ttk.Combobox(
            top,
            values=[
                "Hari Ini",
                "Bulan Ini",
                "Semua"
            ],
            state="readonly",
            width=15
        )

        self.period.current(0)

        self.period.pack(
            side="left"
        )

        tk.Button(
            top,
            text="Tampilkan",
            command=self.load_report
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            top,
            text="Grafik",
            command=self.show_chart
        ).pack(
            side="left"
        )

        self.info = tk.Label(
            self.window,
            text="",
            font=("Arial", 15, "bold")
        )

        self.info.pack(
            pady=10
        )

        columns = (
            "id",
            "tanggal",
            "meja",
            "total",
            "metode"
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

    def get_condition(self):

        period = self.period.get()

        if period == "Hari Ini":

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            return (
                "DATE(tanggal)=?",
                [today]
            )

        elif period == "Bulan Ini":

            month = datetime.now().strftime(
                "%Y-%m"
            )

            return (
                "strftime('%Y-%m', tanggal)=?",
                [month]
            )

        return ("1=1", [])

    def load_report(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        condition, params = self.get_condition()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT
                transaksi.id,
                transaksi.tanggal,
                meja.nomor_meja,
                transaksi.total,
                transaksi.metode_pembayaran
            FROM transaksi
            LEFT JOIN meja
            ON transaksi.meja_id = meja.id
            WHERE transaksi.status='Lunas'
            AND {condition}
            ORDER BY transaksi.id DESC
        """, params)

        rows = cursor.fetchall()

        total = 0

        for row in rows:

            total += row["total"]

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["tanggal"],
                    row["nomor_meja"],
                    f"Rp {row['total']:,.0f}",
                    row["metode_pembayaran"]
                )
            )

        conn.close()

        self.info.config(
            text=(
                f"Total Transaksi: {len(rows)}    |    "
                f"Total Penjualan: Rp {total:,.0f}"
            )
        )

    def show_chart(self):

        condition, params = self.get_condition()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT
                DATE(tanggal) AS tanggal,
                SUM(total) AS total
            FROM transaksi
            WHERE status='Lunas'
            AND {condition}
            GROUP BY DATE(tanggal)
            ORDER BY tanggal
        """, params)

        rows = cursor.fetchall()

        conn.close()

        if not rows:
            return

        dates = [
            row["tanggal"]
            for row in rows
        ]

        totals = [
            row["total"]
            for row in rows
        ]

        plt.figure(
            figsize=(9, 5)
        )

        plt.plot(
            dates,
            totals,
            marker="o"
        )

        plt.title(
            "Grafik Penjualan CaféKu"
        )

        plt.xlabel(
            "Tanggal"
        )

        plt.ylabel(
            "Penjualan (Rp)"
        )

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()

        plt.show()