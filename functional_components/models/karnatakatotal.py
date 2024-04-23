from keras.models import load_model
import numpy as np
import pandas as pd
from keras import preprocessing
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
import matplotlib.pyplot as plt


scaler = MinMaxScaler()

# Load the saved model
model = load_model(r'D:\KRK Datathon\datathon\functional_components\originalmodels\karnatakatotal.keras')
dfkarnataka = pd.read_csv(r"D:\KRK Datathon\datathon\functional_components\originalcsvs\karnataka_total_count.csv",index_col='year_month',parse_dates=True)
dfkarnataka.index.freq='MS'

scaler.fit(dfkarnataka)
scaled = scaler.transform(dfkarnataka)
test_predictions = []

n_input = 12
n_features = 1

first_eval_batch = scaled[-n_input:]
current_batch = first_eval_batch.reshape((1, n_input, n_features))

input_month = int(input("Enter the number of months you want to predict: "))

for i in range(input_month):
    
    # get the prediction value for the first batch
    current_pred = model.predict(current_batch)[0]
    
    # append the prediction into the array
    test_predictions.append(current_pred) 
    
    # use the prediction to update the batch and remove the first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)
    
future_dates = pd.date_range(start=dfkarnataka.index[-2], periods=input_month+1, freq='ME')[1:]
    
for i,j in zip(future_dates, test_predictions):
    print(i, j)
    
true_predictions = scaler.inverse_transform(test_predictions)
# Create a range of future dates for plotting

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(dfkarnataka.index, dfkarnataka['count'], label='Past Values')
plt.plot(future_dates, true_predictions, label='Predicted Values')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Past and Predicted Values')
plt.legend()
plt.show()