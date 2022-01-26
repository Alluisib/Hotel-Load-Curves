import tkinter as tk
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

EnginePower = {}
NumOfEngines = 0
'''
#####This is for Diesel Electric Engines

SFOC = {}

root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300)
canvas1.pack()

label1 = tk.Label(root, text='Please enter the Number of Engines you have')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Type your Number:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def getSquareRoot():
    NumOfEngines = entry1.get()

    canvas1.create_window(200, 230)


button1 = tk.Button(text='Submit', command=getSquareRoot)
canvas1.create_window(200, 180, window=button1)

root.mainloop()


print(NumOfEngines)
'''

SFOCS_AT_DGLOAD = np.array([298.4115125,
279.2831,
263.4103375,
250.4888,
240.2140625,
232.2817,
226.3872875,
222.2264,
219.4946125,
217.8875,
217.1006375,
216.8296,
216.7699625,
216.6173,
216.0671875,
214.8152,
212.5569125,
208.9879,
203.8037375
])

DG_LOAD = np.array([5,
10,
15,
20,
25,
30,
35,
40,
45,
50,
55,
60,
65,
70,
75,
80,
85,
90,
95
])

LNG_SFOC =np.array([455.4263406,
330.3449,
254.9260219,
213.2488,
192.9769531,
184.9347,
182.6826344,
182.0936,
180.9285656,
178.4125,
174.8102469,
171.0024,
168.0611781,
166.8263,
167.4808594,
169.1272,
169.3627906,
163.8561,
145.9224719
])

def SFOC_LOAD(x):
    return 116.393055 * np.exp(-0.054498085 * x) + 210.725125

'''
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

popt, pcur = curve_fit(func, DG_LOAD, SFOCS_AT_DGLOAD)
print(popt)
plt.plot(DG_LOAD, func(DG_LOAD, *popt), 'r-')
plt.scatter(DG_LOAD, SFOCS_AT_DGLOAD)
plt.show()
'''


'''define a user form for entry of engine amx loads
def engine_config():
  '''

def hfo_conversion(quantity_HFO):
    return quantity_HFO*3.096

def mgo_conversion(quantity_MGO):
    return quantity_MGO*3.1672

def lng_conversion(quantity_LNG):
    return quantity_LNG*3.0382

def conversion_func(row):

    for i, temp in enumerate(row):
        if temp >= 80:
            row[i] = 3.096
        else:
            row[i] = 3.1672
    return row


engines = np.array([9000,9000,9000,9000])