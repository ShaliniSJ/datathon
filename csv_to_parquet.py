import pandas as pd

files = ['Predictive Crime Analytics/AccusedData.csv', 'Predictive Crime Analytics/ComplainantDetailsData.csv', 'Predictive Crime Analytics/VictimInfoDetails.csv', 'Predictive Crime Analytics/FIR_Details_Data.csv']
for i in files:
# Load CSV file into a pandas DataFrame
    df = pd.read_csv(i)

    # Convert DataFrame to Parquet format
    df.to_parquet(i.split('.')[0] + '.parquet', engine='pyarrow')
