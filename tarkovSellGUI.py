import tkinter as tk
from tkinter import *
from tkinter import ttk


class karl(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.sex = False
        self.master.title("Karlos")
        self.entry = tk.Entry(text="enter text to print")
        self.button1 = Button(self, text="CLICK HERE", width=25,
                              command=self.print_message)
        self.button2 = Button(self, text="sex HERE", width=25,
                              command=self.sexmachine)
        self.button1.pack()
        self.entry.pack()
        self.button2.pack()

    def sexmachine(self):
        sex = True

    def print_message(self):
        while (self.sex == False):
            print("text")


def main():
    karl().mainloop()


if __name__ == '__main__':
    main()
