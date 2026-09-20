import tkinter as tk
from tkinter import messagebox
from cafeku.database import connect_db


class LoginPage:

    def __init__(self, root, login_success):

        self.root = root
        self.login_success = login_success

        self.frame = tk.Frame(root, bg="#f4f1ea")
        self.frame.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):

        card = tk.Frame(
            self.frame,
            bg="white",
            padx=45,
            pady=40
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            card,
            text="☕ CAFÉKU",
            font=("Arial", 28, "bold"),
            bg="white"
        ).pack()

        tk.Label(
            card,
            text="Cafe Management System",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="Username",
            bg="white",
            anchor="w"
        ).pack(fill="x")

        self.username = tk.Entry(
            card,
            font=("Arial", 12),
            width=30
        )

        self.username.pack(
            pady=(5, 15),
            ipady=7
        )

        tk.Label(
            card,
            text="Password",
            bg="white",
            anchor="w"
        ).pack(fill="x")

        self.password = tk.Entry(
            card,
            font=("Arial", 12),
            show="*",
            width=30
        )

        self.password.pack(
            pady=(5, 20),
            ipady=7
        )

        tk.Button(
            card,
            text="LOGIN",
            font=("Arial", 12, "bold"),
            bg="#6f4e37",
            fg="white",
            width=25,
            pady=8,
            command=self.login
        ).pack()

        tk.Label(
            card,
            text="CaféKu © 2026",
            bg="white",
            fg="gray"
        ).pack(pady=(20, 0))

        self.username.focus()

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

    def login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:

            messagebox.showwarning(
                "Peringatan",
                "Username dan password harus diisi."
            )

            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            self.frame.destroy()

            self.login_success({
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            })

        else:

            messagebox.showerror(
                "Login Gagal",
                "Username atau password salah."
            )