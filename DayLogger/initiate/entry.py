from schedule.gui.probe import Probe
import tkinter as tk

# Author Jadd, Nov 8 2020
# Entry point/ Main()

if __name__ == '__main__':

    application = tk.Tk()

    application.title('ATLAS')
    application.minsize(500, 500)

    application.geometry('1300x800')
    Probe().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
    application.mainloop()
