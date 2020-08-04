# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 20:42:13 2020

@author: SkoczylasKamil
"""

import tkinter as tk
from tkinter import messagebox as msgbox

###################################################################################

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        # stworzyć widgety z tego poziomu, żeby się nie bawić w 1000 definicji
        self.LoadTimeSeries = self.typical_frame("se", "black", "Load time series", self.say_hi)
        self.Forecast = self.typical_frame("sw", "blue", "Twój stary", self.say_hi)
        
        self.create_end_frame()

    def typical_frame(self, anchor_t, color, b_text, command):
        typical_frame = tk.Frame(root, bg = color, borderwidth = 1)
        typical_frame.pack()
        typical_frame.place(x=160, y=110, anchor=anchor_t, width=150, height=100)
        
        typical_button = tk.Button(typical_frame)
        typical_button["text"] = b_text
        typical_button["command"] = command
        typical_button.pack(side = "top")
        #rozbudować o typical button


    def create_end_frame(self):
        self.EndFrame = tk.Frame(root, bg = "red", borderwidth = 1)
        self.EndFrame.pack()
        self.EndFrame.place(x=160, y=110, anchor="nw", width=150, height=100)
        
        self.EndButton = tk.Button(self.EndFrame, text="Quit Program", fg="blue",
                              command=self.master.destroy)
        self.EndButton.pack(side = "bottom")
        
        

    def forecast_settings_window(self):
        self.ForecastFrame

    def say_hi(self):
        msgbox.showinfo("LoL", "Abra kadabra")

###################################################################################

root = tk.Tk()
root.title('NNForecast') 
root.geometry('600x400') 

app = Application(master = root)
app.mainloop()
    


