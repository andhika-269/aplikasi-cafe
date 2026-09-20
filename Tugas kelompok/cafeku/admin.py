import tkinter as tk
from tkinter import ttk, messagebox
from cafeku.database import connect_db

class AdminPage:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title(
            "CaféKu - Admin"
        )

        self.window.geometry(
            "850x600"
        )

        self.create_widgets()
        self.load_users()

    def create_widgets(self):

        form = tk.LabelFrame(
            self.window,
            text="Kelola User",
            padx=15,
            pady=15
        )

        form.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            form,
            text="Username"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.username = tk.Entry(
            form,
            width=25
        )

        self.username.grid(
            row=0,
            column=1,
            padx=10
        )

        tk.Label(
            form,
            text="Password"
        ).grid(
            row=0,
            column=2
        )

        self.password = tk.Entry(
            form,
            width=25
        )

        self.password.grid(
            row=0,
            column=3,
            padx=10
        )

        tk.Label(
            form,
            text="Role"
        ).grid(
            row=1,
            column=0,
            pady=15
        )

        self.role = ttk.Combobox(
            form,
            values=[
                "Admin",
                "Kasir",
                "Waiter",
                "Pembeli",
                "Pemilik"
            ],
            state="readonly",
            width=22
        )

        self.role.grid(
            row=1,
            column=1
        )

        tk.Button(
            form,
            text="Tambah User",
            command=self.add_user,
            bg="#4caf50",
            fg="white"
        ).grid(
            row=1,
            column=3
        )

        columns = (
            "id",
            "username",
            "password",
            "role"
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

        tk.Button(
            self.window,
            text="Hapus User",
            command=self.delete_user,
            bg="#f44336",
            fg="white"
        ).pack(
            pady=10
        )

    def load_users(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            ORDER BY id
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["username"],
                    row["password"],
                    row["role"]
                )
            )

    def add_user(self):

        username = self.username.get().strip()
        password = self.password.get().strip()
        role = self.role.get()

        if not username or not password or not role:

            messagebox.showwarning(
                "Peringatan",
                "Semua data harus diisi."
            )

            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users
                (username, password, role)
                VALUES (?, ?, ?)
            """, (
                username,
                password,
                role
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Berhasil",
                "User berhasil ditambahkan."
            )

            self.username.delete(
                0,
                tk.END
            )

            self.password.delete(
                0,
                tk.END
            )

            self.role.set("")

            self.load_users()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Gagal menambahkan user:\n{e}"
            )

    def delete_user(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Peringatan",
                "Pilih user."
            )

            return

        user_id = self.tree.item(
            selected[0]
        )["values"][0]

        username = self.tree.item(
            selected[0]
        )["values"][1]

        if username == "admin":

            messagebox.showwarning(
                "Tidak Diizinkan",
                "Akun admin utama tidak dapat dihapus."
            )

            return

        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Hapus user {username}?"
        )

        if not confirm:
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id=?",
            (user_id,)
        )

        conn.commit()
        conn.close()

        self.load_users()