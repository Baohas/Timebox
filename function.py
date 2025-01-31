"""from tkinter import *
from tkinter import messagebox #всплывающие окна
window = Tk()
window.title("АРАРАРАРАР")
window.geometry("800x800") #размер окна
frame = Frame(window, padx = 10, pady = 10)
frame.pack(expand = True)
dollar_label = Label(frame, text="$")
dollar_label.grid(row=0, column=0)
rub_label = Label(frame, text="₽")
rub_label.grid(row=1, column=0)
dollar_input = Entry(frame)
dollar_input.grid(row=0, column=1)
rub_input = Entry(frame)
rub_input.grid(row=1, column=1)
def info():
    dollar = int(dollar_input.get())
    rubles = dollar * 97.81
    m=Message(frame,
              text=f"{dollar} долларов = {rubles} рублей")
    m.grid(row=2, column=1)
btn = Button(frame, text="Convert", command = info)
btn.grid(row=2, column=1)
window.mainloop()"""
#два поля для ввода, одно для долларов, другое для рублей + кнопка
import customtkinter as ct
import os
import time
import datetime
from typing import Callable

from pygame.examples.go_over_there import event


class Timebox(ct.CTkFrame):
    def __init__(self, *args, width=150, height=75, step=1,
                 min_value, max_value, command: Callable = None,
                 **kwargs):
        self.min_value = min_value, self.max_value = max_value
        super().__init__(*args, width=width, height=height, **kwargs)
        self.step_size = step
        self.command = command
        self.configure(fg_color=("#fb04c7", "#fb04c7"))
        self.entry = ct.CTkEntry(self, width=150, height=50,
                                 border_width=0, font=("Arial", 50))
        self.entry.grid(row=0, column=0, rowspan=1, columnspan=2)
        self.entry.insert(0, "00")
        self.entry.bind("<MouseWheel>", self.on_mouse_wheel)
        self.entry.bind("<Key>", self.breake)
        self.entry.bind("<Button-1>", self.breake)
        self.entry.bind("<Button-2>", self.breake)
        self.entry.bind("<Enter>", self.enter)
        self.entry.bind("<Leave>", self.leave)
    def breake(self):
        return "break"
    def enter(self, event):
        event.widget.configure(cursor = "hand2")
    def leave(self, event):
        event.widget.configure(cursor="xterm")
    def add_btn_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            value1 = str(value).zfill(2)
            if value>=self.min_value:
                self.entry.delete(0, "end")
                self.entry.insert(0, value1)
        except TypeError:
            return