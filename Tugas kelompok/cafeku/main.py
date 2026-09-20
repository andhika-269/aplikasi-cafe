import tkinter as tk

from cafeku.database import initialize_database
from cafeku.login import LoginPage
from dashboard import Dashboard


class CafeApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "CaféKu - Cafe Management System"
        )

        self.root.geometry(
            "1100x650"
        )

        self.root.minsize(
            900,
            600
        )

        initialize_database()

        self.show_login()

    def show_login(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        LoginPage(
            self.root,
            self.login_success
        )

    def login_success(self, user):

        Dashboard(
            self.root,
            user,
            self.logout
        )

    def logout(self):

        self.show_login()


if __name__ == "__main__":

    root = tk.Tk()

    app = CafeApp(root)

    root.mainloop()