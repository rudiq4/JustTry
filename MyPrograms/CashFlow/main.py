import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Додати', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редагувати', command=self.open_update_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.update_img)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=("ID", "description", "cost", "total"), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('cost', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Найменування')
        self.tree.heading('cost', text='Дохід/Витрата')
        self.tree.heading('total', text='Вартість')

        self.tree.pack()

    def records(self, description, cost, total):
        self.db.insert_data(description, cost, total)
        self.view_records()

    def update_record(self, description, cost, total):
        self.db.c.execute('''UPDATE finance SET description=?, cost=?, total=? WHERE ID=?''',
                          (description, cost, total, self.tree.set(self.tree.selection()[0], '#1')))  # UPDATE - edit
        self.db.conn.commit()  # Save information in database
        self.view_records()  # Up to date new info after changes

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')  # execute - SQL request
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавити дохід/росхід')
        self.geometry('400x200+400+300')
        self.resizable(False, False)

        label_description = ttk.Label(self, text="Найменування: ")
        label_description.place(x=50, y=50)
        label_select = ttk.Label(self, text="Дохід/Витрата: ")
        label_select.place(x=50, y=80)
        label_sum = ttk.Label(self, text="Сума: ")
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)
        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)
        self.combobox = ttk.Combobox(self, values=[u'Дохід', u'Витрата'])
        self.combobox.current(0)  # default value
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавити')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                       self.combobox.get(), self.entry_money.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):  # inherit
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редагувати')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                         self.combobox.get(),
                                                                         self.entry_money.get()))
        self.btn_ok.destroy()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance (id integer primary key, description text, cost text, total real)''')
        self.conn.commit()

    def insert_data(self, description, cost, total):
        self.c.execute('''INSERT INTO finance (description, cost, total) VALUES (?, ?, ?)''',
                       (description, cost, total))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('E-Wallet')
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
