import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from cafeku.database import connect_db
import shutil
import os


class MenuManager:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title("CaféKu - Manajemen Menu")
        self.window.geometry("950x600")

        self.create_widgets()
        self.load_menu()

    def create_widgets(self):

        form = tk.LabelFrame(
            self.window,
            text="Data Menu",
            padx=10,
            pady=10
        )

        form.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(form, text="Nama Menu").grid(
            row=0, column=0, sticky="w"
        )

        self.nama = tk.Entry(form, width=25)
        self.nama.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Kategori").grid(
            row=0, column=2, sticky="w"
        )

        self.kategori = ttk.Combobox(
            form,
            values=[
                "Makanan",
                "Snack",
                "Minuman"
            ],
            state="readonly",
            width=18
        )

        self.kategori.grid(
            row=0,
            column=3,
            padx=5
        )

        tk.Label(form, text="Harga").grid(
            row=1,
            column=0,
            sticky="w",
            pady=10
        )

        self.harga = tk.Entry(
            form,
            width=25
        )

        self.harga.grid(
            row=1,
            column=1
        )

        tk.Label(form, text="Stok").grid(
            row=1,
            column=2
        )

        self.stok = tk.Entry(
            form,
            width=20
        )

        self.stok.grid(
            row=1,
            column=3
        )

        self.foto = ""

        tk.Button(
            form,
            text="Upload Foto",
            command=self.upload_foto
        ).grid(
            row=2,
            column=0,
            pady=10
        )

        self.foto_label = tk.Label(
            form,
            text="Belum ada foto"
        )

        self.foto_label.grid(
            row=2,
            column=1,
            columnspan=2
        )

        button_frame = tk.Frame(form)
        button_frame.grid(row=2, column=3)

        tk.Button(
            button_frame,
            text="Tambah",
            command=self.add_menu,
            bg="#4caf50",
            fg="white"
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="Edit",
            command=self.edit_menu,
            bg="#2196f3",
            fg="white"
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="Hapus",
            command=self.delete_menu,
            bg="#f44336",
            fg="white"
        ).pack(side="left", padx=3)

        # SEARCH
        search_frame = tk.Frame(self.window)
        search_frame.pack(
            fill="x",
            padx=15
        )

        tk.Label(
            search_frame,
            text="Cari:"
        ).pack(side="left")

        self.search = tk.Entry(
            search_frame,
            width=30
        )

        self.search.pack(
            side="left",
            padx=5
        )

        tk.Button(
            search_frame,
            text="Cari",
            command=self.load_menu
        ).pack(side="left")

        # TABLE
        columns = (
            "id",
            "nama",
            "kategori",
            "harga",
            "stok",
            "status",
            "foto"
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "nama": "Nama",
            "kategori": "Kategori",
            "harga": "Harga",
            "stok": "Stok",
            "status": "Status",
            "foto": "Foto"
        }

        for col in columns:

            self.tree.heading(
                col,
                text=headings[col]
            )

        self.tree.column("id", width=40)
        self.tree.column("nama", width=180)
        self.tree.column("kategori", width=100)
        self.tree.column("harga", width=100)
        self.tree.column("stok", width=70)
        self.tree.column("status", width=100)
        self.tree.column("foto", width=150)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.tree.bind(
            "<Double-1>",
            self.select_menu
        )

    def upload_foto(self):

        file = filedialog.askopenfilename(
            title="Pilih Foto Menu",
            filetypes=[
                ("Image", "*.jpg *.jpeg *.png")
            ]
        )

        if not file:
            return

        filename = os.path.basename(file)

        destination = os.path.join(
            "images",
            "menu",
            filename
        )

        shutil.copy2(
            file,
            destination
        )

        self.foto = destination

        self.foto_label.config(
            text=filename
        )

    def load_menu(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        keyword = self.search.get().strip()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM menu
            WHERE nama LIKE ?
            ORDER BY id DESC
        """, (f"%{keyword}%",))

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["nama"],
                    row["kategori"],
                    f"Rp {row['harga']:,.0f}",
                    row["stok"],
                    row["status"],
                    row["foto"] or "-"
                )
            )

    def clear_form(self):

        self.nama.delete(0, tk.END)
        self.harga.delete(0, tk.END)
        self.stok.delete(0, tk.END)
        self.kategori.set("")

        self.foto = ""

        self.foto_label.config(
            text="Belum ada foto"
        )

    def add_menu(self):

        nama = self.nama.get().strip()
        kategori = self.kategori.get()
        harga = self.harga.get().strip()
        stok = self.stok.get().strip()

        if not nama or not kategori or not harga or not stok:

            messagebox.showwarning(
                "Peringatan",
                "Semua data harus diisi."
            )

            return

        try:
            harga = float(harga)
            stok = int(stok)
        except ValueError:

            messagebox.showerror(
                "Error",
                "Harga harus angka dan stok harus bilangan."
            )

            return

        status = "Tersedia" if stok > 0 else "Habis"

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO menu
            (nama, kategori, harga, stok, foto, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nama,
            kategori,
            harga,
            stok,
            self.foto,
            status
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Berhasil",
            "Menu berhasil ditambahkan."
        )

        self.clear_form()
        self.load_menu()

    def select_menu(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.nama.delete(0, tk.END)
        self.nama.insert(0, values[1])

        self.kategori.set(values[2])

        self.harga.delete(0, tk.END)
        self.harga.insert(
            0,
            str(values[3]).replace("Rp ", "").replace(",", "")
        )

        self.stok.delete(0, tk.END)
        self.stok.insert(0, values[4])

        self.foto = "" if values[6] == "-" else values[6]

        self.foto_label.config(
            text=os.path.basename(self.foto)
            if self.foto else "Belum ada foto"
        )

    def edit_menu(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Peringatan",
                "Pilih menu terlebih dahulu."
            )

            return

        menu_id = self.tree.item(
            selected[0]
        )["values"][0]

        try:
            harga = float(self.harga.get())
            stok = int(self.stok.get())
        except ValueError:

            messagebox.showerror(
                "Error",
                "Harga atau stok tidak valid."
            )

            return

        status = "Tersedia" if stok > 0 else "Habis"

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE menu
            SET nama=?,
                kategori=?,
                harga=?,
                stok=?,
                foto=?,
                status=?
            WHERE id=?
        """, (
            self.nama.get(),
            self.kategori.get(),
            harga,
            stok,
            self.foto,
            status,
            menu_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Berhasil",
            "Menu berhasil diperbarui."
        )

        self.clear_form()
        self.load_menu()

    def delete_menu(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Peringatan",
                "Pilih menu terlebih dahulu."
            )

            return

        menu_id = self.tree.item(
            selected[0]
        )["values"][0]

        confirm = messagebox.askyesno(
            "Konfirmasi",
            "Hapus menu ini?"
        )

        if not confirm:
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM menu WHERE id=?",
            (menu_id,)
        )

        conn.commit()
        conn.close()

        self.clear_form()
        self.load_menu()