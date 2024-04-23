import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.preprocessing import MinMaxScaler
from keras import preprocessing
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

dffir = pd.read_csv(r"D:\KRK Datathon\datathon\Predictive Crime Analytics\FIR_Details_Data.csv")
dffir['year_month'] = pd.to_datetime(dffir['Year'].astype(str) + '-' + dffir['Month'].astype(str), format='%Y-%m')

badamipsmotornonfatal_count = dffir[(dffir['CrimeGroup_Name'] == 'MOTOR VEHICLE ACCIDENTS NON-FATAL') & (dffir['UnitName'] == 'Badami PS')].groupby('year_month').size().to_frame(name='count')
idx = pd.date_range(start=dffir['year_month'].min(), end=dffir['year_month'].max(), freq='MS')
badamipsmotornonfatal_count = badamipsmotornonfatal_count.reindex(idx, fill_value=0)
badamipsmotornonfatal_count.index.name = 'year_month'

badamipsmotornonfatal_count = badamipsmotornonfatal_count.sort_values(by='year_month')
badamipsmotornonfatal_count.drop(badamipsmotornonfatal_count.tail(1).index,inplace=True)
badamipsmotornonfatal_count.to_csv('badamipsmotornonfatal_count.csv', index=True)

dfbadamipsmotornonfatal = pd.read_csv("badamipsmotornonfatal_count.csv",index_col='year_month',parse_dates=True)
dfbadamipsmotornonfatal.index.freq='MS'

scaler = MinMaxScaler()
scaler.fit(dfbadamipsmotornonfatal)
scaled = scaler.transform(dfbadamipsmotornonfatal)

n_input = 12
n_features = 1
generator = TimeseriesGenerator(scaled, scaled, length=n_input, batch_size=1)

# define model
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# fit model
model.fit(generator,epochs=50)
model.save("badamipsmotornonfatal.keras")