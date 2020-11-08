import tkinter as tk
import schedule.construct.data_arrange as data

from ..construct.layer import Layer
from calendar import monthrange
from datetime import date
from time import strftime

# Author Jadd, Nov 8 2020
# This class is to display days in a series of months

class MonthSet(Layer):

    # Initialize GUI features
    def __init__(self, *args, **kwargs):
        Layer.__init__(self, *args, **kwargs)

        self.BG = '#222'
        self.FG = '#333'
        self.TEXT = 'white'

        self.real_year = int(date.today().strftime('%Y'))
        self.real_month = int(date.today().strftime('%m'))
        self.real_day = int(date.today().strftime('%d'))

        self.month_tools = tk.Frame(self, bg=self.FG, highlightthickness=0)
        self.real_time = tk.Label(self.month_tools, font='Courier 40', bg=self.FG, fg=self.TEXT)

        self.select_month = tk.Scale(self.month_tools, from_=1, to=12, resolution=1, highlightthickness=0, length=200,
                                font='verdana 10', bg=self.FG, activebackground=self.FG, fg=self.TEXT, width=20,
                                label='Month', orient=tk.HORIZONTAL,
                                command=lambda e: self.draw_monthtable(self.select_year.get(), self.select_month.get()))

        self.select_year = tk.Scale(self.month_tools, from_=2000, to=2100, resolution=1, highlightthickness=0,
                                    length=200, font='verdana 10', bg=self.FG, activebackground=self.FG, fg=self.TEXT,
                                    width=20, label='Year',  orient=tk.HORIZONTAL,
                                    command=lambda e: self.draw_monthtable(self.select_year.get(),self.select_month.get()))

        self.delete_all = tk.Button(self.month_tools, width=20, text='ERASE ALL TASKS', font='Verdana 10 bold', bd=0,
                                    bg="#3A3A3A", fg=self.TEXT, activebackground=self.FG,
                                    activeforeground=self.TEXT, command=lambda: data.delete_all())

        self.schedule = tk.Canvas(self, highlightthickness=0, bg=self.BG)
        self.time_frame = tk.Frame(self.schedule)
        self.schedule.create_window((75, 0), window=self.time_frame, anchor=tk.NW)
        self.clock()
        self.style_obj()


    def clock(self):

        current_time = strftime('%H:%M:%S  ')
        current_time = current_time + str(self.real_day) + '|' + str(self.real_month) + '|' + str(self.real_year)
        self.real_time.config(text=current_time)
        self.real_time.after(1000, self.clock)


    def style_obj(self):

        self.configure(bg=self.BG)
        self.select_year.set(self.real_year)
        self.select_month.set(self.real_month)

        self.real_time.pack(side=tk.LEFT, padx=5)
        self.select_month.pack(side=tk.RIGHT, padx=5)
        self.select_year.pack(side=tk.RIGHT, padx=5)

        self.delete_all.pack(side=tk.RIGHT, padx=0, expand=tk.TRUE)
        self.month_tools.pack(fill=tk.X, expand=tk.FALSE, padx=0, pady=20)
        self.schedule.pack(fill=tk.BOTH, expand=tk.TRUE, padx=0, pady=0)

    # Displays user productivity in color in a series of days
    def draw_monthtable(self, selected_year, selected_month):

        def rate_productivity():
                day_canvas = tk.Canvas(self.day_map, bg=self.FG, height=110, width=155, highlightbackground=self.BG)

                # If statement to ensure days is in range of month
                if (single_day == week_day or self.day_of_month > 1) and (self.day_of_month <= monthrange(selected_year, selected_month)[1]):
                    day_canvas.create_text(15, 15, text=self.day_of_month, font='Verdana 12', fill='white')

                    try:

                        task_list = timetable_day[self.day_of_month]
                        month_tasks = 0
                        productive_hours = 0

                        # Add productive hours
                        for index in range(len(task_list)):
                            if task_list[index].get_perspective() == 'LOG' and task_list[index].get_category() == 'PRODUCTIVE':
                                productive_hours += task_list[index].get_duration()

                        if productive_hours < 3: day_canvas.config(bg='red')
                        elif 3 <= productive_hours < 5: day_canvas.config(bg='#8D8')
                        elif 5 <= productive_hours < 10: day_canvas.config(bg='#3C3')
                        elif productive_hours >= 10: day_canvas.config(bg='dark green')

                        if month_tasks == 0: raise KeyError
                    except KeyError: pass

                    self.day_of_month += 1
                day_canvas.pack(side=tk.LEFT, expand=tk.FALSE, fill=tk.NONE)

        #------------------------------------------------------------------#

        timetable_day = data.get_tasks(selected_year, selected_month)
        for widget in self.time_frame.winfo_children(): widget.destroy() # Reset Data

        self.day_of_month = 1
        for weeks in range(6):  # This loop creates the weeks

            week_day = date(selected_year, selected_month, 1).weekday()
            self.day_map = tk.Frame(self.time_frame, highlightthickness=0)
            week_day = (week_day+1) % 7

            for single_day in range(7): # This loop accounts for the days in the week
                rate_productivity() # Calculate the number of hours of productive tasks in a day
                self.day_map.pack(fill=tk.Y, expand=tk.TRUE)
