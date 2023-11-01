import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import time

df=pd.read_csv("rct.csv")
df.drop(df.columns[[0]],axis=1,inplace=True)

X=df.drop(["CT"],axis=1)
y=df["CT"]

X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.01,random_state=42)
for i in X_test.index:
	isoc=X_test['iSOC'][i]
	fsoc=X_test['fSOC'][i]
	a=X_test['A'][i]
	v=X_test['V'][i]
	t=X_test['T'][i]
	ct=y_test[i]
	X_train.loc[i]=[isoc,fsoc,a,v,t]
	y_train.loc[i]=ct

dtrain=xgb.DMatrix(X_train,label=y_train)
dtest=xgb.DMatrix(X_test,label=y_test)

mini=100
maxi=0
mina=16
maxa=0
minv=60
maxv=0
mint=50
maxt=0
for i in df.index:
	if(df['iSOC'][i]>maxi):
		maxi=df['iSOC'][i]
	if(df['iSOC'][i]<mini):
		mini=df['iSOC'][i]
	if(df['A'][i]>maxa):
		maxa=df['A'][i]
	if(df['A'][i]<mina):
		mina=df['A'][i]
	if(df['V'][i]>maxv):
		maxv=df['V'][i]
	if(df['V'][i]<minv):
		minv=df['V'][i]
	if(df['T'][i]>maxt):
		maxt=df['T'][i]
	if(df['T'][i]<mint):
		mint=df['T'][i]

stats=[[mini,mina,minv,mint],[maxi+1,maxa,maxv,maxt]]
st = pd.DataFrame(stats, columns=['isoc','A','V','T'])
st.to_csv('stats.csv')

def aavg(isoc,fsoc):
	a=0
	n=0
	for i in df.index:
		if(df['iSOC'][i]==isoc):
			if(df['fSOC'][i]==fsoc):
				a+=df['A'][i]
				n+=1
	if(n>0):
		a=a/n
	return a

def vavg(isoc,fsoc):
	v=0
	n=0
	for i in df.index:
		if(df['iSOC'][i]==isoc):
			if(df['fSOC'][i]==fsoc):
				v+=df['V'][i]
				n+=1
	if(n>0):
		v=v/n
	return v

def tavg(isoc,fsoc):
	t=0
	n=0
	for i in df.index:
		if(df['iSOC'][i]==isoc):
			if(df['fSOC'][i]==fsoc):
				t+=df['T'][i]
				n+=1
	if(n>0):
		t=t/n
	return t

def ctavg(isoc,fsoc):
	ct=0
	n=0
	for i in df.index:
		if(df['iSOC'][i]==isoc):
			if(df['fSOC'][i]==fsoc):
				ct+=df['CT'][i]
				n+=1
	if(n>0):
		ct=ct/n
	return ct

for i in X_test.index:
	X_test.drop(i,axis=0,inplace=True)
	y_test.pop(i)

isoc=mini
i=mini
while(i<=maxi):
	fsoc=isoc+1
	a=aavg(isoc,fsoc)
	v=vavg(isoc,fsoc)
	t=tavg(isoc,fsoc)
	ct=ctavg(isoc,fsoc)
	a=round(a,2)
	v=round(v,2)
	t=round(t,2)
	if(a!=0):
		X_test.loc[len(X_test.index)]=[isoc,fsoc,a,v,t]
		y_test.loc[len(y_test.index)]=ct
	isoc=fsoc
	i+=1

time.sleep(2)

params={"objective":"reg:squarederror","max_depth":6,"eta":0.1,"n_estimators":100,"subsample":0.8,"colsample_bytree":0.8}
model=xgb.train(params,dtrain,num_boost_round=44)
dtrain=xgb.DMatrix(X_train,label=y_train)
dtest=xgb.DMatrix(X_test,label=y_test)
y_pred=model.predict(dtest)
model.save_model("model.json")
# n=60
# for i in range(20,n):
# 	params={"objective":"reg:squarederror","max_depth":6,"eta":0.1,"n_estimators":100,"subsample":0.8,"colsample_bytree":0.8}
# 	model=xgb.train(params,dtrain,num_boost_round=i)
# 	dtrain=xgb.DMatrix(X_train,label=y_train)
# 	dtest=xgb.DMatrix(X_test,label=y_test)

# 	y_pred=model.predict(dtest)

# 	rmse=np.sqrt(mean_squared_error(y_test,y_pred))
# 	print("RMSE(",i,"): %.2f"%rmse)

X_test.to_csv('x_test.csv')
print("---X_TEST VALUES SAVED TO 'X_TEST.CSV'---")
y_test.to_csv('y_test.csv')
print("---Y_TEST VALUES SAVED TO 'Y_TEST.CSV'---")

i=0
for pred in y_pred:
	y_test[i]=pred
	i+=1

y_test.to_csv('y_pred.csv')
print("---Y_PRED VALUES SAVED TO 'Y_PRED.CSV'---")