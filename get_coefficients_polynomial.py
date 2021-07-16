import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
order = 1
filename = 'data.csv'
df = pd.read_csv(filename)
x = df.rssi
y = df.meters
p_array = np.polyfit(x,y,order, rcond= 1e-6)
print(p_array)
