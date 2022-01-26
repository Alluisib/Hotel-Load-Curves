import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv(r'C:\Users\Brian\Desktop\Workstuff\PBI_LayUpFinalFile_Costa Firenze.csv', sep = ';', low_memory = False)

'''
Modules for Hotel load isolation below
'''

def CountEngines(row):
    count = 0
    for x in row:
        if x > 100:
            count+=1
    return count

def Hotel_Load(row):
    return max(row)

#The section below counts the number of engines on and minimizes the datafram to only contain when speed is 0, engine
#   count is 1.  The end Dataframe only contains data on total hotel power, date, ship label, and temperature
df = df[df['Speed']==0]
df = df.reset_index(drop = True)
count_of_engines = []
hotel_load = []

for index, row in df[["DG1_ACTIVE_POWER", "DG2_ACTIVE_POWER", "DG3_ACTIVE_POWER", "DG4_ACTIVE_POWER"]].iterrows():
    count_of_engines.append(CountEngines(row))
    hotel_load.append(Hotel_Load(row))

df['EngineCount'] = count_of_engines
df['Max Hotel Load'] = hotel_load
df=df[df['EngineCount']==1]
df=df[df["Temperature"]<=50]
df=df.reset_index(drop = True)
df = df[['Ship','Date', 'Temperature', 'Max Hotel Load']]


#The below creates an additional label categpoty to clssify if the ship was in lay-up or operation
dict_timeperiods = {"Pre-Lay-up":datetime.datetime(2019, 1, 1, 0,0,0),"Lay-up":datetime.datetime(2020, 3, 1, 0,0,0), "Operational":datetime.datetime(2021, 7, 5, 0,0,0)}
labels = ["None"] * len(df["Date"])
df["Date"] = pd.to_datetime(df['Date'])
for timeperiod in dict_timeperiods:
    for i, date in enumerate(df["Date"]):
        if df["Date"][i] >= dict_timeperiods[timeperiod]:
            labels[i] = timeperiod

df['Status'] = labels

#Plotting hotel load by category
groups = df.groupby("Status")
for name, group in groups:
    plt.scatter(group['Temperature'], group['Max Hotel Load'], label = name, s=.2);
plt.title(df['Ship'][0])
plt.legend()
plt.show()

#For each category we create a new dataframe with the average hotel load at certain temperatures
temperature = pd.DataFrame(np.arange(0,35.5,0.5))
temperature['Pre-Lay-up']= 0
temperature["Lay-up"] = 0
temperature["Operational"] = 0


for name, group in groups:
    temperature_dict = {}

    for x in np.arange(0,35.5,0.5):
        temperature_dict[x] = 0

    #round all temps to nearest 0.5
    group['Temperature'] = round(group['Temperature'] *2)/2
    temperature_df = group.groupby("Temperature")
    for temps, data in temperature_df:
        temperature_dict[temps] = sum(data['Max Hotel Load'])/len(data['Max Hotel Load'])

    for i, temperatures in enumerate(temperature[0]):
        temperature[name][i] = temperature_dict[temperatures]

##Next section fills missing data with trends
mincheck = temperature["Operational"][temperature["Operational"] != 0]
print(min(mincheck))

difference_list = []
old = min(mincheck)
for each in mincheck:
    difference_list.append(each-old)
    old = each

list = [min(mincheck)]*(len(mincheck)-2)
count = 0
adder = 0
for num in difference_list[2:]:
    adder += num
    list[count] += adder
    count+=1

i = 28
listcounter = 0
while i > 1:
    temperature["Operational"][i] = list[listcounter]
    i-=1
    listcounter +=1

plotcheck = temperature["Operational"][temperature["Operational"]!=0].astype(float)

x = np.arange(0,len(plotcheck)/2, 0.5)
plt.plot(x, plotcheck, "o", c = "black")


print(np.polyfit(x, plotcheck, 2))
trendline = np.poly1d(np.polyfit(x, plotcheck, 2))
plt.plot(x, trendline(x), 'r--')
plt.show()


