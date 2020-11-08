from tkinter import Frame

# Author Jadd, Nov 8 2020
# To create an app that can seamlessly cycle through different pages,
# class Layer acts as pages on book which can either be revealed or not

class Layer(Frame):

    def __init__(self, *args, **kwargs): Frame.__init__(self, *args, **kwargs)

    def reveal(self): self.lift()
