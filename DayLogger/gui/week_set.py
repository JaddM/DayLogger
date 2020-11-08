import tkinter as tk
import schedule.construct.data_arrange as data

from .popup.hover_info import HoverInfo
from ..gui.popup.task_addition import TaskAddition
from ..gui.popup.task_deletion import TaskDeletion
from ..construct.layer import Layer

from calendar import monthrange
from datetime import date
from time import strftime

# Author Jadd, Nov 8 2020
# To display all tasks in series of days in the week

class WeekSet(Layer):

    # To initialize all variable, buttons and GUI features
    def __init__(self, *args, **kwargs):
        Layer.__init__(self, *args, **kwargs)

        def ms_wheel(event): self.schedule.yview_scroll(int(-7 * (event.delta/100)), 'units')   # Scroll Control

        self.WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        self.BG = '#222'
        self.FG = '#333'
        self.TEXT = 'white'
        self.BUTTON = '#3A3A3A'

        self.real_year = int(date.today().strftime('%Y'))
        self.real_month = int(date.today().strftime('%m'))
        self.real_day = int(date.today().strftime('%d'))

        self.tools = tk.Frame(self, bg=self.FG, highlightthickness=0)
        self.real_time = tk.Label(self.tools, font='Courier 80', bg=self.FG, fg=self.TEXT)
        self.clock()
        self.average_frame = tk.Frame(self.tools, bg=self.FG)

        self.select_month = tk.Scale(self.tools, from_=1, to=12, resolution=1, highlightthickness=0, length=220,
                                font='verdana 10', bg=self.FG, activebackground=self.FG, fg=self.TEXT, width=20,
                                label='Month', command=lambda e: self.draw_timetable('LOG', self.select_year.get(),
                                self.select_month.get(), self.real_day))

        self.select_year = tk.Scale(self.tools, from_=2000, to=2100, resolution=1, highlightthickness=0, length=220,
                                font='verdana 10', bg=self.FG, activebackground=self.FG, fg=self.TEXT, width=20,
                                label='Year', command=lambda e: self.draw_timetable('LOG', self.select_year.get(),
                                self.select_month.get(), self.real_day))

        self.log = tk.Button(self.tools, width=10, text='LOG', font='Verdana 10 bold', bd=0, bg=self.BUTTON,
                                fg=self.TEXT, activebackground=self.FG, activeforeground=self.TEXT,
                                command=lambda: self.draw_timetable('LOG', self.select_year.get(),
                                self.select_month.get(), self.real_day))

        self.day_schedule = tk.Button(self.tools, width=10, text='SCHEDULE', font='Verdana 10 bold', bd=0,
                                bg=self.BUTTON, fg=self.TEXT, activebackground=self.FG, activeforeground=self.TEXT,
                                command=lambda: self.draw_timetable('SCHEDULE', self.select_year.get(),
                                self.select_month.get(), self.real_day))

        self.schedule = tk.Canvas(self, highlightthickness=0) # 'Schedule' houses the days
        self.schedule.bind_all('<MouseWheel>', ms_wheel)

        self.scrollbox = tk.Frame(self.schedule) # 'Scrollbox' is scrollable window of days
        self.scrollbox.bind('<Configure>', lambda e: self.schedule.configure(scrollregion=self.schedule.bbox("all")))
        self.scroll = tk.Scrollbar(self.schedule, command=self.schedule.yview)

        self.schedule.create_window((0, 0), window=self.scrollbox)
        self.schedule.configure(yscrollcommand=self.scroll.set)
        self.style()

    # Prompts add/delete windows
    def add_task(self): TaskAddition(self)
    def delete_task(self): TaskDeletion(self)

    # Assigns tooltip to visual entity of task
    def attach_hover(self, shape, text):

        hover_obj = HoverInfo(shape)

        def over(event): hover_obj.appear(text)
        def not_over(event): hover_obj.disappear()

        shape.bind('<Enter>', over)
        shape.bind('<Leave>', not_over)


    def clock(self):

        current_time = strftime('%H:%M:%S\n')
        current_time = current_time + str(self.real_day) + '|' + str(self.real_month) + '|' + str(self.real_year)
        self.real_time.config(text=current_time)
        self.real_time.after(1000, self.clock)

    # Calculate the average hours of a certain type of task
    def category_averages(self, category, chosen_year, chosen_month):

        day_allotted = 0
        category_allotted = 0
        timetable_day = data.get_tasks(chosen_year, chosen_month)

        if self.real_year == chosen_year and self.real_month == chosen_month: day_limit = self.real_day
        else: day_limit = monthrange(chosen_year, chosen_month)[1] + 1

        for day in range(1, day_limit):
            for every in range(len(timetable_day[day])):

                if timetable_day[day][every].get_category() == category and timetable_day[day][every].get_perspective() == 'LOG':
                        category_allotted += timetable_day[day][every].get_duration()

            day_allotted += 1
        if day_allotted == 0: return "0";
        return str(round(category_allotted/day_allotted, 2))


    def display_average(self, chosen_year, chosen_month):

        for widget in self.average_frame.winfo_children(): widget.destroy()

        tk.Label(self.average_frame,
                     text='PRODUCTIVE: '+self.category_averages('PRODUCTIVE', chosen_year, chosen_month)+'h/day',
                     bg=self.FG, fg=self.TEXT, font='verdana 8').pack(pady=5)

        tk.Label(self.average_frame,
                     text='LEISURE: '+self.category_averages('LEISURE', chosen_year, chosen_month)+'h/day',
                     bg=self.FG, fg=self.TEXT, font='verdana 8').pack(pady=5)

        tk.Label(self.average_frame,
                     text='SLEEP: '+self.category_averages('SLEEP', chosen_year, chosen_month)+'h/day',
                     bg=self.FG, fg=self.TEXT, font='verdana 8').pack(pady=5)


    def style(self):
        self.configure(bg=self.BG)
        self.select_year.set(self.real_year)
        self.select_month.set(self.real_month)

        self.real_time.pack(side=tk.LEFT, padx=5)

        self.select_month.pack(side=tk.RIGHT)
        self.select_year.pack(side=tk.RIGHT)

        self.log.pack(side=tk.RIGHT, padx=5, pady=5)
        self.day_schedule.pack(side=tk.RIGHT, padx=5, pady=5)
        self.average_frame.pack(expand=tk.TRUE)
        self.tools.pack(fill=tk.X, expand=tk.FALSE, padx=40, pady=10)

        self.schedule.pack(fill=tk.BOTH, expand=tk.TRUE, padx=50, pady=10)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # To Display tasks in colored bars
    def draw_timetable(self, selected_perspective, year_selected, month_selected, highlight_day):

        def draw_bars():
            try:
                for hour in range(24):  # Create 24-hour timeline
                    day_map.create_text(250+hour*40, 20, text=str(hour)+':00', font='Verdana 8', fill=self.TEXT)
                    day_map.create_line(250+40*hour, 250, 250+40*hour, 30, dash=(4, 4), fill=self.TEXT)

                day_tasks = timetable_day.get(single_day)
                for task in range(len(day_tasks)):

                    start = day_tasks[task].get_start_time()
                    if start % 100 != 0: start += 20
                    end = day_tasks[task].get_end_time()
                    if end % 100 != 0: end += 20

                    start = start/100
                    end = end/100

                    # To create bar and hover tooltip
                    if day_tasks[task].get_perspective() == selected_perspective:

                        divide = 220/len(day_tasks)
                        hover_text = 'ID: ' + str(day_tasks[task].get_id()) + '\n' + \
                                         str(day_tasks[task].get_start_time()) + '-' + \
                                         str(day_tasks[task].get_end_time()) + ': ' + \
                                         str(day_tasks[task].get_duration()) + 'h\n\n' + \
                                         day_tasks[task].get_description()

                        bar = tk.Label(day_map, background=day_tasks[task].get_colour()) # Calculate bar dimensions
                        bar.place(x=252+40*start, y=32+divide*task, height=((30+divide*(task+1))-(30+divide*task)-2),
                                        width=((250+40*end)-(250+40*start)-2))
                        self.attach_hover(bar, text=hover_text)

                # Add/Delete buttons
                adds = tk.Button(day_map, width=10, text='ADD', font='Verdana 10', bd=0, bg=self.FG, fg=self.TEXT,
                                     activeforeground=self.TEXT, activebackground=self.FG, command=self.add_task)
                deletes = tk.Button(day_map, width=10, text='DELETE', font='Verdana 10', bd=0, bg=self.FG, fg=self.TEXT,
                                        activeforeground=self.TEXT, activebackground=self.FG, command=self.delete_task)
                day_map.create_window((145, 180), window=adds)
                day_map.create_window((145, 210), window=deletes)

            except KeyError: pass

        #---------------------------------------------------------------#

        self.display_average(year_selected, month_selected)
        timetable_day = data.get_tasks(year_selected, month_selected)
        for widget in self.scrollbox.winfo_children(): widget.destroy()   # Reset data

        # The loop sets up the canvas for visualizing tasks with the date and time
        for single_day in range(1, monthrange(year_selected, month_selected)[1]+1):

            week_day = date(year_selected, month_selected, single_day).weekday()
            day_map = tk.Canvas(self.scrollbox, bg=self.FG, width=1220, height=260,
                                    highlightthickness=1, highlightbackground=self.BG)

            # To highlight real date
            if self.real_month == month_selected and self.real_year == year_selected and single_day == highlight_day:
                day_map.create_text(150, 55, text=self.WEEKDAYS[week_day], font='Verdana 17 bold', fill='gold')
                day_map.create_text(145, 130, text=single_day, font='Verdana 40 bold', fill='gold')

            else:
                day_map.create_text(150, 55, text=self.WEEKDAYS[week_day], font='Verdana 17', fill=self.TEXT)
                day_map.create_text(145, 130, text=single_day, font='Verdana 22', fill=self.TEXT)

            day_map.create_text(145, 90, text='('+selected_perspective+')', font='Verdana 10', fill=self.TEXT)
            draw_bars()
            day_map.pack()
