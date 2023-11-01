import pandas as pd
import xgboost as xgb

df=pd.read_csv("rct.csv")
df.drop(df.columns[[0]],axis=1,inplace=True)

X=df.drop(["CT"],axis=1)
y=df["CT"]

model = xgb.Booster()
model.load_model("model.json")
# SHAP ANALYSIS
import shap
nopython=False
import shap
from shap import TreeExplainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X, plot_type='bar')
shap.summary_plot(shap_values, X)
shap.dependence_plot(1, shap_values, X, interaction_index="iSOC")
shap.dependence_plot(2, shap_values, X, interaction_index="iSOC")
shap.dependence_plot(3, shap_values, X, interaction_index="iSOC")
shap.dependence_plot(4, shap_values, X, interaction_index="iSOC")
