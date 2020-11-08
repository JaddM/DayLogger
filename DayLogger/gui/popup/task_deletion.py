from tkinter import messagebox
import tkinter as tk
import schedule.construct.data_arrange as data

# Author Jadd, Nov 8 2020
# Window for task deletion

class TaskDeletion:

    def __init__(self, parent):

            def to_delete():
                try:
                    data.delete_db(int(task_delete.get()))
                except ValueError:
                    messagebox.showerror('ERROR', 'ID must be an INTEGER!')
                delete_window.destroy()

            delete_window = tk.Toplevel(parent)
            delete_window.title('DEL')
            delete_window.configure(bg='#333333')
            delete_window.geometry('200x100')

            delete_label = tk.Label(delete_window, text='Enter Task ID', font='verdana 10', bg='#333', fg='white')
            task_delete = tk.Entry(delete_window, highlightthickness=0, width=15, font='verdana 10', bg='#BBB')

            delete_label.pack(pady=3)
            task_delete.pack(pady=3)
            task_delete.focus_set()

            delete_button = tk.Button(delete_window, text='DELETE', command=to_delete)
            delete_button.pack()
