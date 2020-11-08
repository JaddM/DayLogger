import tkinter as tk
from tkinter import messagebox
import schedule.construct.data_arrange as data

from calendar import monthrange
from datetime import date, datetime

# Author Jadd, Nov 8 2020
# Window for task input

class TaskAddition:

    # Initialize GUI features
    def __init__(self, parent):
        def to_add():

            if monthrange(self.task_year.get(), self.task_month.get())[1] < self.task_day.get():
                    messagebox.showerror('ERROR', 'The day you have CHOSEN DOES NOT EXIST')

            else:
                data.write_db(self.task_year.get(), self.task_month.get(), self.task_day.get(),
                              self.start_hour.get()+self.start_minute.get(),self.end_hour.get()+self.end_minute.get(),
                              self.perspective_val.get(), self.category_val.get(), self.task_description.get())

                self.add_window.destroy()

        self.real_year = int(date.today().strftime('%Y'))
        self.real_month = int(date.today().strftime('%m'))
        self.real_day = int(date.today().strftime('%d'))

        self.add_window = tk.Toplevel(parent)
        self.date_container = tk.Frame(self.add_window)

        self.start_hour = tk.Scale(self.add_window, from_=0, to=2400, resolution=100, orient=tk.HORIZONTAL,
                    highlightthickness=0, length=300, font='verdana 10', bg='#333333', activebackground='#333333',
                    fg='white', width=20, label='Start : Hour ↓↓↓')
        self.start_minute = tk.Scale(self.add_window, from_=0, to=30, resolution=30, orient=tk.HORIZONTAL,
                    highlightthickness=0, length=120, font='verdana 10', bg='#333333', activebackground='#333333',
                    fg='white', width=20, label='Start : Minute↓')
        self.end_hour = tk.Scale(self.add_window, from_=0, to=2400, resolution=100, orient=tk.HORIZONTAL,
                    highlightthickness=0, length=300, font='verdana 10', bg='#333333', activebackground='#333333',
                    fg='white', width=20, label='End : Hour ↓↓↓')
        self.end_minute = tk.Scale(self.add_window, from_=0, to=30, resolution=30, orient=tk.HORIZONTAL,
                    highlightthickness=0, length=120, font='verdana 10', bg='#333333', activebackground='#333333',
                    fg='white', width=20, label='End : Minute↓')

        self.perspective_label = tk.Label(self.add_window, text='Perspective', font='verdana 10', bg='#333333', fg='white')
        self.perspective_val = tk.StringVar(self.add_window)

        self.task_perspective = tk.OptionMenu(self.add_window, self.perspective_val, "LOG", "SCHEDULE")

        self.category_label = tk.Label(self.add_window, text='Category', font='verdana 10', bg='#333333', fg='white')
        self.category_val = tk.StringVar(self.add_window)

        self.task_category = tk.OptionMenu(self.add_window, self.category_val, "PRODUCTIVE", "LEISURE", "SLEEP")

        self.description_label = tk.Label(self.add_window, text='Description', font='verdana 10', bg='#333333', fg='white')
        self.task_description = tk.Entry(self.add_window, highlightthickness=0, width=60, font='verdana 10', bg='#BBB')

        self.task_month = tk.Scale(self.date_container, from_=1, to=12, resolution=1, highlightthickness=0, length=120,
                            font='verdana 10', bg='#333333', activebackground='#333333', fg='white', width=20,
                            label='Month')
        self.task_year = tk.Scale(self.date_container, from_=2000, to=2100, resolution=1, highlightthickness=0,
                            length=120, font='verdana 10', bg='#333333', activebackground='#333333', fg='white',
                            width=20, label='Year')
        self.task_day = tk.Scale(self.date_container, from_=1, to=31, resolution=1, highlightthickness=0, length=120,
                            font='verdana 10', bg='#333333', activebackground='#333333', fg='white', width=20, label='Day')
        self.add_button = tk.Button(self.add_window, text='ADD', command=to_add)
        self.style()


    def style(self):
        self.add_window.title('ADD')
        self.add_window.configure(bg='#333')
        self.add_window.geometry('600x600')

        self.perspective_val.set("LOG")
        self.task_perspective.config(highlightthickness=0, width=15, font='verdana 10', bg='#777', fg='white')
        self.category_val.set("PRODUCTIVE")
        self.task_category.config(highlightthickness=0, width=15, font='verdana 10', bg='#777', fg='white')

        self.start_hour.set(100 * int(datetime.now().strftime('%H')))
        self.end_hour.set(100 * int(datetime.now().strftime('%H')))

        self.task_day.set(self.real_day)
        self.task_month.set(self.real_month)
        self.task_year.set(self.real_year)

        self.start_hour.pack()
        self.start_minute.pack()
        self.end_hour.pack()
        self.end_minute.pack()

        self.perspective_label.pack(pady=3)
        self.task_perspective.pack()

        self.category_label.pack(pady=3)
        self.task_category.pack()

        self.description_label.pack(pady=3)
        self.task_description.pack()
        self.task_description.focus_set()

        self.date_container.pack(pady=10)
        self.task_day.pack(side=tk.LEFT)
        self.task_month.pack(side=tk.LEFT)
        self.task_year.pack(side=tk.LEFT)

        self.add_button.pack()

