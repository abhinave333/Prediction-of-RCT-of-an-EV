import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

df=pd.read_csv("x_test.csv")
isoc=df['iSOC']
fsoc=df['fSOC']
cur=df['A']
vol=df['V']
tmp=df['T']

mini=100
maxi=0
for i in df.index:
	if(df['iSOC'][i]>maxi):
		maxi=df['iSOC'][i]
	if(df['iSOC'][i]<mini):
		mini=df['iSOC'][i]

ip=np.array(isoc)
fp=np.array(fsoc)
cp=np.array(cur)
vp=np.array(vol)
tp=np.array(tmp)

# CALCULATE
df=pd.read_csv("y_test.csv")
ct=df['CT']

cnt=maxi-mini

cnt=0
for i in df.index:
	cnt+=1

cnt=cnt-1

i=1
while(i<=cnt):
	ct[i]+=ct[i-1]
	i+=1

yp=np.array(ct)

time.sleep(2)

# PREDICT
df=pd.read_csv("y_pred.csv")
pct=df['CT']

i=1
while(i<=cnt):
	pct[i]+=pct[i-1]
	i+=1

xp=np.array(pct)

plt.xlabel("Time(mins)")
plt.ylabel("SOC%")

print("---PLOTTING PREDICTED CT AND CALCULATED CT---")
plt.plot(xp,fp,color='r',marker='o',label='Predicted CT')
plt.plot(yp,fp,color='g',marker='o',label='Calculated CT')
plt.legend()
plt.grid()
plt.xticks(np.arange(0, 440, 10))
plt.yticks(np.arange(0, 105, 5))
plt.show()

plt.plot(ip,cp,marker='o',label='Current')
plt.legend()
plt.grid()
plt.yticks(np.arange(0, 15, 1))
plt.xticks(np.arange(0, 105, 5))
plt.show()

plt.plot(ip,vp,marker='o',label='Voltage')
plt.legend()
plt.grid()
plt.yticks(np.arange(40, 65, 5))
plt.xticks(np.arange(0, 105, 5))
plt.show()

plt.plot(ip,tp,marker='o',label='Temp')
plt.legend()
plt.grid()
plt.yticks(np.arange(25, 45, 5))
plt.xticks(np.arange(0, 105, 5))
plt.show()
