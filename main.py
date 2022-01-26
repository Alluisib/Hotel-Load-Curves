import pandas as pd
import numpy as np
from Engines_SFOC import *

df = pd.read_csv(r'C:\Users\Brian\Desktop\Combined Engine Data - AIDAblu.csv', low_memory=False)
df.info()

mw = df[["DG1_ACTIVE_POWER", "DG2_ACTIVE_POWER", "DG3_ACTIVE_POWER", "DG4_ACTIVE_POWER"]]
temperature = df[["DG1_FUEL_OIL_IN_TE","DG2_FUEL_OIL_IN_TE","DG3_FUEL_OIL_IN_TE","DG4_FUEL_OIL_IN_TE" ]]

SFOC = SFOC_LOAD(mw/engines)
fuel_consumed = mw*SFOC/1000000
time_stamp = 0.05
fuel_consumed = fuel_consumed*time_stamp
fuel_consumed = fuel_consumed.dropna()
temperature = temperature.dropna()

temperature.apply(conversion_func, axis = 1)

co2_produced = np.matmul(np.asarray(fuel_consumed.T), temperature)
i_matrix = np.identity(len(co2_produced))
print(np.sum(np.sum(co2_produced*i_matrix)))
print("Tons of Co2 Produced for " + df["Ship"][0] + " From: " + str(df["Date"][0]) + " To: " + str(df["Date"][len(fuel_consumed)-1]))

