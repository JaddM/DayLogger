import sqlite3
import random

from tkinter import messagebox
from ..construct.task_node import TaskNode
from calendar import monthrange

# Author Jadd, Nov 8 2020
# To collect data needed to assemble visualizations of tasks and scheduling

def get_tasks(year_needed, month_needed):

    conn = sqlite3.connect('tasks.db')
    nav = conn.cursor()

    # To create if needed is non-existent
    try:
        nav.execute("SELECT * FROM tasks WHERE year=? AND month=?", (year_needed, month_needed))

    except sqlite3.OperationalError:
        nav.execute("""CREATE TABLE tasks (
            year integer,
            month integer,
            day integer,
            identity integer,
            start integer,
            end integer,
            perspective text,
            category text,
            description text
            )""")
        nav.execute("SELECT * FROM tasks WHERE year=? AND month=?", (year_needed, month_needed))

    try:
        db_list = nav.fetchall()
        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        messagebox.showerror('ERROR', 'FETCH FROM DATABASE FAILED!')
        return

    # The series of loops below attach a list of tasks to a dictionary where the
    # key is the date and the value is the task list
    list_of_days = {}
    for day in range(1, monthrange(year_needed, month_needed)[1]+1):

        list_of_tasks = []
        for every in range(len(db_list)):

            if db_list[every][2] == day:
                list_of_tasks.append(TaskNode(db_list[every][3], db_list[every][4], db_list[every][5], db_list[every][6],
                                              db_list[every][7], db_list[every][8]))

        list_of_days[day] = list_of_tasks
    return list_of_days


# To insert tasks into database
def write_db(year, month, day, start, end, perspective, category, description):

    try:
        conn = sqlite3.connect('tasks.db')

        nav = conn.cursor()
        nav.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (year, month, day, generate_id(), start, end, perspective, category, description))

        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        messagebox.showerror('ERROR', 'WRITE TO DATABASE FAILED!')


def delete_db(task_id):

    try:
        conn = sqlite3.connect('tasks.db')

        nav = conn.cursor()
        nav.execute("DELETE FROM tasks WHERE identity=?", (task_id,))

        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        messagebox.showerror('ERROR', 'DELETE FROM DATABASE FAILED!')


# To create a unique ID for every task for easy recognition
def generate_id():

    conn = sqlite3.connect('tasks.db')
    nav = conn.cursor()
    for x in range(10001):  # Though looping 10001 time will not account all randoms,
                            # though it indicates it almost exhausted and must be cleared
        identification = random.randint(1, 10000)
        nav.execute("SELECT * FROM tasks WHERE identity=?", (identification,))
        conn.commit()
        db_list = nav.fetchall()

        if len(db_list) == 0:
            conn.close()
            return identification

    messagebox.showerror('ERROR', 'IDs EXHAUSTED!')


def delete_all():

    try:
        conn = sqlite3.connect('tasks.db')

        nav = conn.cursor()
        nav.execute("DROP TABLE tasks")

        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        messagebox.showerror('ERROR', 'DROP TABLE FAILED!')
