import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

filename = 'data.csv'
df = pd.read_csv(filename)
x = df.rssi
y = df.meters

models = []      
mse_hist = []

for order in range(1,6):
    p = (np.poly1d(np.polyfit(x, y, order, rcond=1e-6)))
    models.append(p)
    
    e = np.abs(y-p(x))
    mse = np.sum(e**2)/len(df)
    
    mse_hist.append(mse) 

rssi_series = pd.Series(mse_hist)  

plt.figure(figsize=(20, 10))
ax = rssi_series.plot(kind='bar')
ax.set_xlabel("Degree of the polynomial")
ax.set_ylabel("Mean square error")
ax.set_xticklabels(range(1,6),rotation=0)

rects = ax.patches

for rect in rects:
       y_value = rect.get_height()
       x_value = rect.get_x() + rect.get_width() / 2

       space = 5
       va = 'bottom'
       label = "{:.2f}".format(y_value)

       plt.annotate(
           label,                      
           (x_value, y_value),         
           xytext=(0, space),          
           textcoords="offset points", 
           ha='center',                
           va=va)                      

plt.savefig("image.png")
plt.show()