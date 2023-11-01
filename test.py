import pandas as pd
import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

df=pd.read_csv("x_test.csv")
st=pd.read_csv("stats.csv")
df.drop(df.columns[[0]],axis=1,inplace=True)
df2=pd.read_csv("y_test.csv")
X=df
df2.drop(df2.columns[[0]],axis=1,inplace=True)
y=df2["CT"]

X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.01,random_state=42)

for i in X_test.index:
	X_test.drop(i,axis=0,inplace=True)

for i in y_test.index:
	y_test.pop(i)


soc_min=st.loc[0]['isoc']
current_min=st.loc[0]['A']
voltage_min=st.loc[0]['V']
temp_min=st.loc[0]['T']
soc_max=st.loc[1]['isoc']
current_max=st.loc[1]['A']
voltage_max=st.loc[1]['V']
temp_max=st.loc[1]['T']

print("SOC(MINIMUM):",soc_min)
print("SOC(MAXIMUM):",soc_max)
print("CURRENT(MINIMUM):",current_min)
print("CURRENT(MAXIMUM):",current_max)
print("VOLTAGE(MINIMUM):",voltage_min)
print("VOLTAGE(MAXIMUM):",voltage_max)
print("TEMP(MINIMUM):",temp_min)
print("TEMP(MAXIMUM):",temp_max)

for i in df.index:
    isoc=df['iSOC'][i]
    fsoc=df['fSOC'][i]
    a=df['A'][i]
    v=df['V'][i]
    t=df['T'][i]
    X_test.loc[isoc]=[isoc,fsoc,a,v,t]
    i+=1

print("\n---RCT ESTIMATION---")
while(1):
    isoc=int(input("INITIAL SOC : "))
    fsoc=int(input("FINAL SOC : "))
    a=float(input("CURRENT : "))
    v=float(input("VOLTAGE : "))
    t=float(input("TEMPERATURE : "))
    X_test.loc[isoc]=[isoc,isoc+1,a,v,t]

    si=isoc
    sf=fsoc
    i=si+1
    while(i<80):
        X_test.loc[i]['A']=a
        i+=1

    dtrain=xgb.DMatrix(X_train,label=y_train)
    dtest=xgb.DMatrix(X_test,label=y_test)
    model = xgb.Booster()
    model.load_model("model.json")
    y_pred=model.predict(dtest)
    rct=0
    i=int(si-soc_min)
    sf=int(fsoc-soc_min)
    while(i<sf):
        rct+=y_pred[i]
        i+=1

    h=rct/60
    m=rct%60
    print("RCT FROM ",end="")
    print(si,end="")
    print("% TO ",end="")
    print(fsoc,end="")
    print("%")
    print("%d" %h,"hours","%d" %m,"mins")
    print("\n---RCT ESTIMATION---")
