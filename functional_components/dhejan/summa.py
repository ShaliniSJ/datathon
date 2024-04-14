import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = r"C:\\Users\\Legion\\Desktop\\KSP DATATHON\\datathon\\Predictive Crime Analytics\\FIR_Details_Data.csv"
df = pd.read_csv(file_path)

# Assuming the column containing crime types is named 'Crime_Type', you can filter it like this
crime_column = df['CrimeGroup_Name']

# Print unique crime types
unique_crimes = crime_column.unique()
print(unique_crimes)

