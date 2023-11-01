import pandas as pd
from datetime import datetime
from time import sleep

df=pd.read_csv("get_data.csv")

def diff_time(start_time,end_time):
	end=datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
	start=datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
	d=end-start
	return d.total_seconds()/60

ndf=pd.DataFrame(columns=['iSOC','fSOC','A','V','T','CT'])
df_cnt=0
for i in df.index:
	df_cnt+=1

sleep(2)

i=0
while(i<df_cnt):
	a=0
	v=0
	t=0
	a=df['Current'][i]
	v=df['Voltage'][i]
	t=df['Temp'][i]
	if(df['Status'][i]==1):
		j=i+1
		while(j<df_cnt):
			if(df['Status'][j]==0):
				print("(",j,")")
				i=j
				break
			if((df['SOC'][j]-df['SOC'][i])>1):
				i=j
				break
			a+=df['Current'][j]
			v+=df['Voltage'][j]
			t+=df['Temp'][j]
			if((df['SOC'][j]-df['SOC'][i])==1):
				ct=diff_time(df['Time'][i],df['Time'][j])
				isoc=df['SOC'][i]
				fsoc=df['SOC'][j]
				a=a/(j-i+1)
				v=v/(j-i+1)
				t=t/(j-i+1)
				a=round(a,2)
				v=round(v,2)
				t=round(t,2)
				if(ct<30):
					ndf.loc[len(ndf.index)]=[isoc,fsoc,a,v,t,ct]
				print("[",i,"]->[",j,"]")
				i=j-1
				break
			j=j+1
	i=i+1

sleep(2)

ndf.to_csv('get_ct.csv')

print("---CHARGING TIME FOR EACH 1% SOC CALCULATED AND SAVED TO 'GET_CT.CSV'---")