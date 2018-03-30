# -*- coding: utf-8 -*-
# @Author: Steven
# @Date: 2018-03-29 15:02:06
# @Last Modified by: Steven 
# @Last Modified time: 2018-03-29 16:22:51 
# @file: tkinter_demo01.py

import tkinter as tk
import tkinter.messagebox as messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.height_lable = tk.Label(self, text="Height/cm")
        self.height_lable.grid(row=0, column=0)
        height_value = tk.StringVar()
        height_value.set('170')
        self.height_input = tk.Entry(self, textvariable=height_value)
        self.height_input.grid(row=0, column=2)
        self.weight_lable = tk.Label(self, text="Weight/kg")
        self.weight_lable.grid(row=1, column=0)
        weight_value = tk.StringVar()
        weight_value.set('65')
        self.weight_input = tk.Entry(self, textvariable=weight_value)
        self.weight_input.grid(row=1, column=2)

        self.quit = tk.Button(self, text="Quit", fg='red',
                              command=root.quit)
        self.quit.grid(row=2, column=1, columnspan=2)
        self.submit = tk.Button(self, text="Calulate",
                                command=self.calulate)
        self.submit.grid(row=2, column=0, columnspan=2)

    def calulate(self):
        w = self.weight_input.get()
        h = self.height_input.get()
        bmi = int(w) / ((int(h) / 100)**2)
        print(f'bmi is {bmi:.2f}')
        messagebox.showinfo('Message', f'bmi is {bmi:.2f}')


root = tk.Tk()
root.title('BMI计算器')
root.geometry('300x100')
app = Application(master=root)

app.mainloop()
