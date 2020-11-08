import tkinter as tk
from .week_set import WeekSet
from .month_set import MonthSet

# Author Jadd, Nov 8 2020
# To create a class which is used to navigate through different pages of the application and
# set as the primary frame to house sub-frames

class Probe(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        window = tk.Frame(self)
        week_gui = WeekSet(self)
        month_gui = MonthSet(self)

        choose_month = tk.Frame(self, bg='#222')
        choose_week = tk.Frame(self, bg='#222')
        show_month = tk.Button(choose_month, text='<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<', bd=0, bg='#222', fg='white',
                               activebackground='#222', activeforeground='white', command=month_gui.reveal)
        show_week = tk.Button(choose_week, text='>\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>\n', bd=0, bg='#222', fg='white',
                              activebackground='#222', activeforeground='white', command=week_gui.reveal)

        choose_month.pack(side=tk.LEFT, fill=tk.Y)
        choose_week.pack(side=tk.RIGHT, fill=tk.Y)
        show_month.pack(side=tk.LEFT)
        show_week.pack(side=tk.RIGHT)

        window.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        week_gui.place(in_=window, x=0, y=0, relwidth=1, relheight=1)
        month_gui.place(in_=window, x=0, y=0, relwidth=1, relheight=1)

        week_gui.reveal()
