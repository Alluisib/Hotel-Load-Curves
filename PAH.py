import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import timedelta

df_dg3 = pd.read_csv(r'C:\Users\Brian\Desktop\Workstuff\20210909_DG3_Compliance_Report.csv',encoding='UTF-16 LE', sep= '\t')
df_dg4 = pd.read_csv(r'C:\Users\Brian\Desktop\Workstuff\20210909_DG4_Compliance_Report.csv',encoding='UTF-16 LE', sep= '\t')
df_AIDAprima = pd.read_csv(r'C:\Users\Brian\Desktop\Workstuff\data_AIDAprima.csv')

df_dg4.info()
df_dg3.info()
df_AIDAprima.info()


dict_timeperiod = {"Post-Octamar":datetime.datetime(2021, 9, 1, 0,0,0)}
list = df_dg3.columns
df_clean_dg3 = df_dg3[['Date & Time UTC', 'DG3 Load [%]', 'DG3 SW Flow to DeSOx [m³/h]', 'DG3 PAH at DeSOx Outlet [ppb]']]
df_clean_dg4 = df_dg4[['Date & Time UTC', 'DG4 Load [%]', 'DG4 SW Flow to DeSOx [m³/h]', 'DG4 PAH at DeSOx Outlet [ppb]']]
df_AIDAprima_clean = df_AIDAprima[['Date', 'Sum of Temperature', 'Speed']]

#Convert Date time
i=0
df_clean_dg3['Date & Time UTC_new'] = 0
for date in df_clean_dg3['Date & Time UTC']:
    df_clean_dg3['Date & Time UTC_new'][i] = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    i+=1

i=0
df_clean_dg4['Date & Time UTC_new'] = 0
for date in df_clean_dg4['Date & Time UTC']:
    df_clean_dg4['Date & Time UTC_new'][i] = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
    i+=1

i=0
df_AIDAprima_clean['Date & Time UTC_new'] = 0
for date in df_AIDAprima['Date']:
    df_AIDAprima_clean['Date & Time UTC_new'][i] = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M')
    i+=1

df_AIDAprima_clean['Date & Time UTC_new'] = df_AIDAprima_clean['Date & Time UTC_new'] + timedelta(seconds = 60)
datelist = [df_clean_dg4['Date & Time UTC_new'].iloc[0],df_clean_dg4['Date & Time UTC_new'].iloc[-1]]
indexlist = [0,0]
i=0
for date in datelist:
        indexlist[i] = df_AIDAprima_clean.loc[df_AIDAprima_clean['Date & Time UTC_new'] == date]
        i+=1

df_AIDAprima_clean.drop(index = df_AIDAprima_clean.iloc[0:6714], inplace=True)
df_AIDAprima_clean.drop(index = df_AIDAprima_clean.iloc[18823:], inplace=True)
print(df_AIDAprima_clean)

df_clean_dg4['Octamar'] = np.where(df_clean_dg4['Date & Time UTC_new'] < dict_timeperiod["Post-Octamar"], 0, 1)
df_clean_dg3['Octamar'] = np.where(df_clean_dg3['Date & Time UTC_new'] < dict_timeperiod["Post-Octamar"], 0, 1)

pd.merge(df_clean_dg3, df_AIDAprima_clean, on = "Date $ Time UTC_new")
pd.merge(df_clean_dg4, df_AIDAprima_clean, on = "Date $ Time UTC_new")
