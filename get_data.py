import pandas as pd
from time import sleep

# STATUS
print("---PROCESSING 'STATUS.CSV'---")

statusdf=pd.read_csv("status.csv")
for i in statusdf.index:
	fg=0
	if(statusdf['Time'][i][17]=='0' or statusdf['Time'][i][17]=='3'):
		if(statusdf['Time'][i][18]=='0'):
			fg=1
			print("[",i,"]->[",statusdf['Time'][i],"]")
	elif(statusdf['Time'][i][17]=='1' or statusdf['Time'][i][17]=='4'):
		if(statusdf['Time'][i][18]=='5'):
			fg=1
			print("[",i,"]->[",statusdf['Time'][i],"]")
	if(fg==0):
		statusdf.drop(i,axis=0,inplace=True)

sleep(2)

# SOC
print("---PROCESSING 'SOC.CSV'---")

socdf=pd.read_csv("soc.csv")
df=pd.DataFrame(columns=['Time','SOC','Status'])
n=0
for n in socdf.index:
	n+=1

l=0
for i in statusdf.index:
	flag=0
	j=l
	while(j<n):
		if(statusdf['Time'][i]==socdf['Time'][j]):
			t=statusdf['Time'][i]
			sc=socdf['soc'][j]
			st=statusdf['charging_status'][i]
			flag=1
			l=j
			break
		elif(statusdf['Time'][i]<socdf['Time'][j]):
			break
		j+=1
	if(flag==1):
		df.loc[len(df.index)]=[t,sc,st]
	print("[",i,"]->[",j,"]->[",flag,"]")

df.to_csv('get_data1.csv')

sleep(2)

# CURRENT
print("---PROCESSING 'CURRENT.CSV'---")

cdf=pd.read_csv("current.csv")
for i in cdf.index:
	if(cdf['charge current'][i]>100):
		c=cdf['charge current'][i]
		c=c/1000
		cdf['charge current'][i]=c
	print("[",i,"]")

sleep(2)

df=pd.DataFrame(columns=['Time','SOC','Status','Current'])
statusdf=pd.read_csv("get_data1.csv")
n=0
for n in cdf.index:
	n+=1
	
l=0
for i in statusdf.index:
	flag=0
	j=l
	while(j<n):
		if(statusdf['Time'][i]==cdf['Time'][j]):
			t=statusdf['Time'][i]
			sc=statusdf['SOC'][i]
			st=statusdf['Status'][i]
			c=cdf['charge current'][j]
			flag=1
			l=j
			break
		elif(statusdf['Time'][i]<cdf['Time'][j]):
			break
		j+=1
	if(flag==1):
		df.loc[len(df.index)]=[t,sc,st,c]
	print("[",i,"]->[",j,"]->[",flag,"]")

df.to_csv('get_data2.csv')

sleep(2)

# VOLTAGE
print("---PROCESSING 'VOLTAGE.CSV'---")

vdf=pd.read_csv("voltage.csv")
statusdf=pd.read_csv("get_data2.csv")
df=pd.DataFrame(columns=['Time','SOC','Status','Current','Voltage'])
n=0
for n in vdf.index:
	n+=1

l=0
for i in statusdf.index:
	flag=0
	j=l
	while(j<n):
		if(statusdf['Time'][i]==vdf['Time'][j]):
			t=statusdf['Time'][i]
			sc=statusdf['SOC'][i]
			st=statusdf['Status'][i]
			c=statusdf['Current'][i]
			v=vdf['dc_voltage'][j]
			flag=1
			l=j
			break
		elif(statusdf['Time'][i]<vdf['Time'][j]):
			break
		j+=1
	if(flag==1):
		df.loc[len(df.index)]=[t,sc,st,c,v]
	print("[",i,"]->[",j,"]->[",flag,"]")

df.to_csv('get_data3.csv')

sleep(2)

# TEMPERATURE
print("---PROCESSING 'TEMP.CSV'---")

tdf=pd.read_csv("temp.csv")
statusdf=pd.read_csv("get_data3.csv")
df=pd.DataFrame(columns=['Time','SOC','Status','Current','Voltage','Temp'])
n=0
for n in tdf.index:
	n+=1

l=0
fi=0
for i in statusdf.index:
	flag=0
	t=statusdf['Time'][i]
	sc=statusdf['SOC'][i]
	st=statusdf['Status'][i]
	c=statusdf['Current'][i]
	v=statusdf['Voltage'][i]
	j=l
	while(j<n):
		if(statusdf['Status'][i]==0):
			break
		if(statusdf['Time'][i]==tdf['Time'][j]):
			temp=tdf['charging battery temp'][j]
			flag=1
			l=j
			break
		j+=1
	if(flag==1):
		df.loc[len(df.index)]=[t,sc,st,c,v,temp]
		fi=0
	else:
		temp=0
		if(fi==0):
			df.loc[len(df.index)]=[t,sc,st,c,v,temp]
			fi=1
	print("[",i,"]->[",j,"]->[",flag,"]")

df.to_csv('get_data.csv')

sleep(2)

print("---ALL PARAMETERS COMBINED AND SAVED TO 'GET_DATA.CSV'---")
