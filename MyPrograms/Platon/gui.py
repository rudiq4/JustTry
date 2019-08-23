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

        toolbar = tk.Frame(bg='#3895D3', bd=3)
        toolbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        '''buttons'''
        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, command=self.open_dialog, bg='#1261A0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.TOP)

        self.edit_img = tk.PhotoImage(file='edit.gif')
        btn_edit_dialog = tk.Button(toolbar, command=self.open_update_dialog, bg='#1261A0', bd=0,
                                    compound=tk.TOP, image=self.edit_img)
        btn_edit_dialog.pack(side=tk.TOP)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar,command=self.delete_records, bg='#1261A0', bd=0,
                               compound=tk.TOP, image=self.delete_img)
        btn_delete.pack(side=tk.TOP)

        '''tree(plate, brand, model, region)'''

        self.tree = ttk.Treeview(self, columns=("ID", "plate", "brand", "model", "region"), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('plate', width=150, anchor=tk.CENTER)
        self.tree.column('brand', width=150, anchor=tk.CENTER)
        self.tree.column('model', width=150, anchor=tk.CENTER)
        self.tree.column('region', width=200, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('plate', text='Держ. номер')
        self.tree.heading('brand', text='Марка')
        self.tree.heading('model', text='Модель')
        self.tree.heading('region', text='Область')

        self.tree.pack()

    def records(self, plate, brand, model, region):
        self.db.insert_data(plate, brand, model, region)
        self.view_records()

    def update_record(self, plate, brand, model, region):
        self.db.c.execute('''UPDATE plates SET plate=?, brand=?, model=?, region=? WHERE ID=?''',
                          (plate, brand, model, region, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()  # Save information in database
        self.view_records()  # Up to date new info after changes

    def view_records(self):
        self.db.c.execute('''SELECT * FROM plates''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for item in self.tree.selection():
            self.db.c.execute('''DELETE FROM plates WHERE id=?''', (self.tree.set(item, '#1'),))
            self.db.conn.commit()
            self.view_records()

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
        self.title('Добавити номер')
        self.geometry('400x230+400+300')
        self.resizable(False, False)

        label_plate = ttk.Label(self, text="Номер: ")
        label_plate.place(x=50, y=50)
        label_brand = ttk.Label(self, text="Марка: ")
        label_brand.place(x=50, y=80)
        label_model = ttk.Label(self, text="Модель: ")
        label_model.place(x=50, y=110)
        label_model = ttk.Label(self, text="Область: ")
        label_model.place(x=50, y=140)

        self.entry_plate = ttk.Entry(self)
        self.entry_plate.place(x=200, y=50)
        self.entry_brand = ttk.Entry(self)
        self.entry_brand.place(x=200, y=80)
        self.entry_model = ttk.Entry(self)
        self.entry_model.place(x=200, y=110)
        self.entry_region = ttk.Entry(self)
        self.entry_region.place(x=200, y=140)
        # self.combobox = ttk.Combobox(self, values=[u'Дохід', u'Витрата'])
        # self.combobox.current(0)  # default value
        # self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавити')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_plate.get(),
                                                                       self.entry_brand.get(), self.entry_model.get(),
                                                                       self.entry_region.get()))

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
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_plate.get(),
                                                                       self.entry_brand.get(), self.entry_model.get(),
                                                                       self.entry_region.get()))
        self.btn_ok.destroy()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('plates.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS plates (id integer primary key, plate text, brand text, model text,
             region text)''')
        self.conn.commit()

    def insert_data(self, plate, brand, model, region):
        self.c.execute('''INSERT INTO plates (plate, brand, model, region) VALUES (?, ?, ?, ?)''',
                       (plate, brand, model, region))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Генератор номерних знаків')
    root.geometry("800x450+300+200")
    root.resizable(False, False)
    root.mainloop()
