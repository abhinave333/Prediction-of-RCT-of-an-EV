PYTHON LIBRARIES REQUIERED

pip install pandas
pip install numpy
pip install xgboost
pip install scikit-learn
pip install datetime
pip install shap
pip install matplotlib


GET_DATA.PY 	//Combining all the parametes of a dataset to a single csv file
CALCULATE.PY 	//Calculating charging time for each 1% soc range
CREATE_MODEL.PY //Train the xgboost model and save the model as a json file
SHAPAY.PY 	//Shap analysis on the dataset and model
PLOT.PY 	//Plot the avg values for different parameters and predicted output
TEST.PY 	//Testing the model with a given input

rct.CSV		//Contains the caculated charging time for each 1% soc range of all the datasets
x_test.csv	//Contains the parameters used for testing the model
y_test.csv	//Calculated charging time of the test values
y_pred.csv	//Predicted charging time of the test values
data.csv	//Parameters for testing the model
stats.csv	//Contains maximum and minimum values of all parameters in the dataset

MODEL.JSON	//Trained model containing the data about the best iteration and weights of the model