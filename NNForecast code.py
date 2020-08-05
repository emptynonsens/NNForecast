# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 20:42:13 2020

@author: SkoczylasKamil
"""

import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import filedialog
############################# NEURAL NETWORKS #################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import *
from keras.layers import *
import os
import tensorflow as tf
from tensorflow import *


def sieci_neuronowe():
    
    dataset = pd.read_csv(r'C:\Users\Kamil\Desktop\Dane - imput.csv',header = 0, index_col = 0)
    
    
    dataset.head()
    
    df = pd.DataFrame(dataset)
    dfm1 = df.shift(-1)
    
    dfm1['wig0']= df['wig']
    
    reframed = dfm1[:-1303]
    
    values = reframed.values #teraz wartosci to już nasza próba t-1 i t
    podział = round(len(values) * 0.2) # próba ucząca 80%
    
    train = values[podział:,:] # próba ucząca x, y
    
    test = values[:podział,:] # próba testowa
    
    train_X, train_y = train[:, :-1], train[:, -1] # tu dla x ucinamy jedną z prawej i a dla y bieżemy jedną z prawej
    
    test_X, test_y = test[:, :-1], test[:, -1] # to samo dla danych testowych, tylko ze krótsza próba
    
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1])) # zmiana kształtu macieży 
    
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    
    
    
    
    model = Sequential() #tworzymy model ogólny
    # dodajemy pierwszą warstwę 32 neurony, z pamięcią długoterminową
    model.add(LSTM(5,return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2]))) # do modelu dodajemy kształt, czyli 1 obserwacja (timestep), 3 dane
    model.add(Dropout(0.3))
    model.add(LSTM(5))
    model.add(Dropout(0.2))
    # dodajemy warstwę 1, wyjsciową y
    model.add(Dense(1,))
    model.compile(loss='mse', optimizer='adam')
    
    
    history = model.fit(train_X, train_y, epochs=500, batch_size=126, validation_data=(test_X, test_y), verbose=2, shuffle=False)
    
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()
    
    yhat = model.predict(test_X)
    prognoza = pd.DataFrame(yhat)
    wynik = pd.DataFrame(test)
    wynik = wynik.rename(columns = {0:'WIG-1',1:'DJ-1',2:'USD/PLN-1',3:'WIG0'})
    
    wynik['WIG0P']= prognoza
     # predykcja dla konkretnej daty
    
    wynik['zgodny kierunek'] = np.where((wynik['WIG0'] < 0) & (wynik['WIG0P'] < 0) | (wynik['WIG0'] > 0) & (wynik['WIG0P'] > 0), 1 , 0)
    wynik
    
    skutecznosc = wynik['zgodny kierunek'].sum()/wynik['zgodny kierunek'].count()
    return skutecznosc.astype('|S5')
###################################################################################

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        # stworzyć widgety z tego poziomu, żeby się nie bawić w 1000 definicji
        self.LoadTimeSeries = self.typical_frame("se", "black", "Load time series", self.import_danych)
        self.Forecast = self.typical_frame("sw", "blue", "Twój stary", self.fill_in_textbox)
        self.text_box
        
        self.create_end_frame()
       # self.frame1.text_box.insert(tk.END, "Wut a fu u u u u k")

    def import_danych(self):
        self.plik =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("CSV Files","*.csv"),("all files","*.*")))
        self.T1 = self.text_box(self.plik, 210)
        
        t = sieci_neuronowe()
        print(t)
        
        
        self.T2 = self.text_box(t, 260)
    
    def fill_in_textbox(self):
        self.text_box("Nie ogarniam tego za bardzo, więc zrobię jak umiem", 210)        
        
    def say_hi(self):
        msgbox.showinfo("LoL", "Abra kadabra")
        
    def text_box(self, text, placeY):
        H = 40
        W = 300
        frame1 = tk.Frame(root, bg = "white", borderwidth = 1)
        frame1.pack()
        frame1.place(x=10, y=placeY, anchor= "nw", width = W, height=H)
        
        text_box = tk.Text(frame1, height=H, width=W)
        text_box.pack()
        text_box.insert(tk.END, text)

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



###################################################################################

root = tk.Tk()
root.title('NNForecast') 
root.geometry('600x400') 

app = Application(master = root)
app.mainloop()
    

# importujemy pliki



