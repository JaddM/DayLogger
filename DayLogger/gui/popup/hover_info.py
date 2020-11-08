import tkinter as tk

# Author Jadd, Nov 8 2020
# This class creates a popup that gives a description of the task when hovered over

class HoverInfo(object):

    def __init__(self, shape):

        self.__shape = shape
        self.__hover_box = None

    def appear(self, description):

        self.__description = description
        if self.__hover_box or not self.__description: return

        x, y, cx, cy = self.__shape.bbox("insert")
        x = x + self.__shape.winfo_rootx() + 57
        y = y + cy + self.__shape.winfo_rooty() + 27

        self.__hover_box = window = tk.Toplevel(self.__shape)
        window.wm_overrideredirect(1)
        window.wm_geometry("+%d+%d" % (x - 175, y))

        label = tk.Label(window, text=self.__description, justify=tk.LEFT, background="white", relief=tk.SOLID, borderwidth=0,
                         font='tahoma 10')
        label.pack(ipadx=1)

    def disappear(self):

        window = self.__hover_box
        self.__hover_box = None
        if window: window.destroy()
