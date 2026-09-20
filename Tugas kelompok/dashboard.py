import tkinter as tk
from tkinter import messagebox

# tes github

class Dashboard:

    def __init__(self, root, user, logout):

        self.root = root
        self.user = user
        self.logout = logout

        self.create_dashboard()

    def create_dashboard(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(
            f"CaféKu - Dashboard {self.user['role']}"
        )

        self.root.geometry("1100x650")

        # HEADER
        header = tk.Frame(
            self.root,
            bg="#6f4e37",
            height=70
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="☕ CAFÉKU",
            font=("Arial", 22, "bold"),
            bg="#6f4e37",
            fg="white"
        ).pack(
            side="left",
            padx=25,
            pady=18
        )

        tk.Label(
            header,
            text=f"{self.user['username']} | {self.user['role']}",
            font=("Arial", 11),
            bg="#6f4e37",
            fg="white"
        ).pack(
            side="right",
            padx=25
        )

        # BODY
        body = tk.Frame(
            self.root,
            bg="#f4f1ea"
        )

        body.pack(
            fill="both",
            expand=True
        )

        # SIDEBAR
        sidebar = tk.Frame(
            body,
            bg="#33251d",
            width=220
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        tk.Label(
            sidebar,
            text="MENU",
            font=("Arial", 12, "bold"),
            bg="#33251d",
            fg="white"
        ).pack(pady=20)

        self.add_sidebar_buttons(sidebar)

        # CONTENT
        self.content = tk.Frame(
            body,
            bg="#f4f1ea"
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.show_welcome()

    def add_button(self, parent, text, command):

        tk.Button(
            parent,
            text=text,
            command=command,
            bg="#4a3628",
            fg="white",
            relief="flat",
            anchor="w",
            padx=20,
            pady=12
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

    def add_sidebar_buttons(self, sidebar):

        role = self.user["role"]

        if role == "Admin":

            self.add_button(
                sidebar,
                "📋 Kelola Menu",
                self.open_menu
            )

            self.add_button(
                sidebar,
                "👥 Kelola User",
                self.open_admin
            )

            self.add_button(
                sidebar,
                "📊 Laporan",
                self.open_laporan
            )

            self.add_button(
                sidebar,
                "🪑 Meja",
                self.open_kasir
            )

        elif role == "Kasir":

            self.add_button(
                sidebar,
                "💳 Pembayaran",
                self.open_kasir
            )

            self.add_button(
                sidebar,
                "📊 Penjualan Hari Ini",
                self.open_laporan
            )

        elif role == "Waiter":

            self.add_button(
                sidebar,
                "🍽 Pesanan",
                self.open_waiter
            )

        elif role == "Pembeli":

            self.add_button(
                sidebar,
                "🍔 Pesan Menu",
                self.open_order
            )

        elif role == "Pemilik":

            self.add_button(
                sidebar,
                "📊 Laporan Penjualan",
                self.open_laporan
            )

        self.add_button(
            sidebar,
            "🚪 Logout",
            self.confirm_logout
        )

    def show_welcome(self):

        tk.Label(
            self.content,
            text=f"Selamat Datang di CaféKu",
            font=("Arial", 28, "bold"),
            bg="#f4f1ea"
        ).pack(pady=(100, 10))

        tk.Label(
            self.content,
            text=f"Login sebagai {self.user['role']}",
            font=("Arial", 15),
            bg="#f4f1ea"
        ).pack()

        tk.Label(
            self.content,
            text="Gunakan menu di sebelah kiri untuk mengakses sistem.",
            font=("Arial", 11),
            bg="#f4f1ea",
            fg="gray"
        ).pack(pady=10)

    def open_menu(self):

        from menu import MenuManager

        MenuManager(self.root)

    def open_order(self):

        from order import OrderPage

        OrderPage(self.root, self.user)

    def open_waiter(self):

        from waiter import WaiterPage

        WaiterPage(self.root)

    def open_kasir(self):

        from kasir import KasirPage

        KasirPage(self.root)

    def open_laporan(self):

        from laporan import LaporanPage

        LaporanPage(self.root)

    def open_admin(self):

        from cafeku.admin import AdminPage

        AdminPage(self.root)

    def confirm_logout(self):

        result = messagebox.askyesno(
            "Logout",
            "Apakah kamu yakin ingin logout?"
        )

        if result:
            self.logout()