import tkinter as tk
from tkinter import ttk
import mysql.connector


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
        btn_open_dialog = tk.Button(toolbar, text='Додати позицію', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=(
            'ID', 'description', 'costs', 'total'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Назва')
        self.tree.heading('costs', text='Стаття доходу\росходу')
        self.tree.heading('total', text='Сума')

        self.tree.pack()


    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)
        self.view_records()

    def view_records(self):
        self.db.c.execute("SELECT * FROM finance")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Додати доходи\росходи')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Назва:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Стаття доходу\росходу:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сума:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Дохід', u'Росхід'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Додати', command=self.destroy)
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                  self.combobox.get(),
                                                                  self.entry_money.get()))

        self.grab_set()
        self.focus_set()


class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='root',
            password='',
            host='127.0.0.1',
            port='3306'
        )
        self.c = self.conn.cursor()
        self.c.execute("CREATE DATABASE IF NOT EXISTS finances")
        self.c.execute("USE finances")
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS finance (id INT AUTO_INCREMENT PRIMARY KEY, description VARCHAR(255), costs VARCHAR(255), total INT)")
        self.conn.commit()

    def insert_data(self, description, costs, total):
        self.c.execute("INSERT INTO finance(description, costs, total) VALUES (%s, %s, %s)",
                       (description, costs, total))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Household finance")
    root.geometry("650x525+400+200")

    label_resume = tk.Label(text='ПІБ : Мізера Владислав Олегович',font=40)
    label_resume.place(x=20, y=435)
    label_resume = tk.Label(text='Номер : 380(68)0507380',font=40)
    label_resume.place(x=20, y=465)
    s = tk.StringVar()
    s.set('Резюме : https://goo.su/1wfp')
    entry = tk.Entry(root, text=s,bd=0,font=40,width=23)
    entry.place(x=20, y=495)

    root.resizable(False, False)
    root.mainloop()
