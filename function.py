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
# два поля для ввода, одно для долларов, другое для рублей + кнопка
import customtkinter as ct
import os
import time
import datetime
from typing import Callable


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
        event.widget.configure(cursor="hand2")

    def leave(self, event):
        event.widget.configure(cursor="xterm")

    def add_btn_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            value1 = str(value).zfill(2)
            if value >= self.min_value:
                self.entry.delete(0, "end")
                self.entry.insert(0, value1)
        except TypeError:
            return

    def subtract_btn_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            value1 = str(value).zfill(2)
            if value >= self.min_value:
                self.entry.delete(0, "end")
                self.entry.insert(0, value1)
        except TypeError:
            return

    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return 0

    def on_mouse_wheel(self, event):
        if not self.timer_running:
            if event.delta > 0:
                self.add_btn_callback()
            else:
                self.subtract_btn_callback()

    def start_timer(self):
        self.timer_running = True
        self.unbind("<MouseWheel>")

    def stop_timer(self):
        self.timer_running = False
        self.bind("<MouseWheel>", self.on_mouse_wheel)

    def set(self, value: int):
        value1 = str(value).zfill(2)
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value1))


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        ct.set_default_color_theme("green")
        self.title("Авто-выключатель")
        self.geometry(f"{520}x{260}")
        # главный кадр
        self.main_frame = ct.CTkFrame(self, width=520, height=260)
        self.main_frame.grid(row=0, column=0, rowspan=10,
                             columnspan=10)
        self.main_frame.rowconfigure(3, weight=1)
        # меню опций
        self.optionmenu1 = ct.CTkOptionMenu(self.main_frame,
                                            values=["Shutdown",
                                                    "Reboot", "Sleep", "Logout"], font=("Arial", 20),
                                            fg_color=("#ff0000", "#0000ff"), text_color="#fff",
                                            button_color=("#000", "#fff"))
        self.optionmenu1.grid(row=0, column=1)
        self.optionmenu1.set("After")
        self.optionmenu2 = ct.CTkOptionMenu(self.main_frame,
                                            values=["Shutdown", "Reboot", "Sleep", "Logout"],
                                            font=("Arial", 20), fg_color=("#ff0000", "#0000ff"),
                                            text_color="#fff", button_color=("#000", "#fff"))
        self.optionmenu2.grid(row=0, column=0)
        self.optionmenu2.set("Shutdown")
        # Buttons
        self.start_button = ct.CTkButton(self.main_frame,
                                         text="Start", command=self.mod)
        self.start_button.grid(row=0, column=5)
        self.cancel_button = ct.CTkButton(self.main_frame,
                                          text="Cancel", command=self.cancel_shutdown)
        self.cancel_button.grid(row=0, column=6)
        self.switch_var = ct.StringVar()
        self.switch_mode = ct.CTkSwitch(self.main_frame,
                                        text="Dark", variable=self.switch_var, onvalue="on",
                                        offvalue="off", command=self.change_appearance)
        self.switch_mode.grid(row=5, column=0)
        # таймбоксы
        self.timebox_hours = Timebox(self.main_frame,
                                     min_value=0, max_value=23, step=1, fg_color="transparent")
        self.timebox_hours.grid(row=1, column=0)
        self.timebox_mins = Timebox(self.main_frame, min_value=0,
                                    max_value=59, step=1, fg_color="transparent")
        self.timebox_mins.grid(row=1, column=2)
        self.timebox_seconds = Timebox(self.main_frame, min_value=0,
                                       max_value=59, step=1, fg_color="transparent")
        self.timebox_seconds.grid(row=1, column=4)
        self.label1 = ct.CTkLabel(self.main_frame, text=":",
                                  fg_color="transparent")
        self.label1.grid(row=1, column=1)
        self.label2 = ct.CTkLabel(self.main_frame, text=":",
                                  fg_color="transparent")
        self.label1.grid(row=1, column=3)
        # flags
        self.active = bool(None)
        self.pause = False
        self.backup = 0
        self.timebox_hours.timer_running = False
        self.timebox_mins.timer_running = False
        self.timebox_seconds.timer_running = False

    def update_label_time(self, shutdown_time):
        if self.active is True:
            self.timebox_hours.timer_running = True
            self.timebox_mins.timer_running = True
            self.timebox_seconds.timer_running = True
            if shutdown_time <= 0:
                if self.optionmenu2.get() == "Shutdown":
                    self.shutdown()
                elif self.optionmenu2.get() == "Reboot":
                    self.suspend()
                elif self.optionmenu2.get() == "Sleep":
                    self.sleep()
                    self.destroy()
                elif self.optionmenu2.get() == "Logout":
                    self.logout()
                    self.destroy()
            else:
                hours, reminder = divmod(shutdown_time, 3600)
                mins, seconds = divmod(reminder, 60)
                self.timebox_hours.set(hours)
                self.timebox_mins.set(mins)
                self.timebox_seconds.set(seconds)
