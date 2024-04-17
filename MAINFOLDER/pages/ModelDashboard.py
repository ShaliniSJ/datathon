import json
import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

def predict_crime(selected_unit, selected_crime, selected_district, input_month, selected_date):
    scaler = MinMaxScaler()

    # Load the saved model
    # model = load_model('../../originalmodels/karnatakatotal.keras')        
    
    if selected_crime == "ALL" and selected_district == "ALL" and selected_unit=="ALL":
        model = load_model(r'originalmodels\karnatakatotal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\karnataka_total_count.csv',index_col='year_month',parse_dates=True)
        
    elif selected_crime == "MOTOR VEHICLE ACCIDENTS NON-FATAL" and selected_district == "Bagalkot" and selected_unit=="Amengad PS":
        model = load_model(r'originalmodels\amengadpsmotornonfatal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\amengadpsmotornonfatal_count.csv',index_col='year_month',parse_dates=True)
        
    elif selected_crime == "MOTOR VEHICLE ACCIDENTS NON-FATAL" and selected_district == "Bagalkot" and selected_unit=="Badami PS":
        model = load_model(r'originalmodels\badamipsmotornonfatal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\badamipsmotornonfatal_count.csv',index_col='year_month',parse_dates=True)
    
    elif selected_crime == "MOTOR VEHICLE ACCIDENTS NON-FATAL" and selected_district == "Bagalkot" and selected_unit=="ALL":
        model = load_model(r'originalmodels\bagalkotmotornonfatal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\bagalkotmotornonfatal_count.csv',index_col='year_month',parse_dates=True) 
        
    elif selected_crime == "MOTOR VEHICLE ACCIDENTS NON-FATAL" and selected_district == "Ballari" and selected_unit=="ALL":
        model = load_model(r'originalmodels\ballarimotornonfatal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\ballarimotornonfatal_count.csv',index_col='year_month',parse_dates=True)  
        
    elif selected_crime == "MOTOR VEHICLE ACCIDENTS NON-FATAL" and selected_district == "Belagavi City" and selected_unit=="ALL":
        model = load_model(r'originalmodels\belagavicitymotornonfatal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\belagavicitymotornonfatal_count.csv',index_col='year_month',parse_dates=True) 
        
    elif selected_crime == "MOTOR VEHICLE ACCIDENTS NON-FATAL" and selected_district == "Bengaluru City" and selected_unit=="ALL":
        model = load_model(r'originalmodels\bengalurucitymotornonfatal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\bengalurucitymotornonfatal_count.csv',index_col='year_month',parse_dates=True)
    
    elif selected_crime == "KIDNAPPING AND ABDUCTION" and selected_district == "ALL" and selected_unit=="ALL":
        model = load_model(r'originalmodels\karnatakakidnapping.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\karnataka_kidnapping_count.csv',index_col='year_month',parse_dates=True)
        
    elif selected_crime == "POCSO" and selected_district == "ALL" and selected_unit=="ALL":
        model = load_model(r'originalmodels\karnatakaposco.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\karnataka_pocso_count.csv',index_col='year_month',parse_dates=True)
        
    elif selected_crime == "MOTOR VEHICLE ACCIDENTS NON-FATAL" and selected_district == "ALL" and selected_unit=="ALL":
        model = load_model(r'originalmodels\karnatakamotornonfatal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\karnataka_motornonfatal_count.csv',index_col='year_month',parse_dates=True)
        
    elif selected_crime == "THEFT" and selected_district == "ALL" and selected_unit=="ALL":
        model = load_model(r'originalmodels\karnatakatheft.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\karnataka_theft_count.csv',index_col='year_month',parse_dates=True)
        
    else:
        model = load_model(r'originalmodels\karnatakatotal.keras')
        dfkarnataka = pd.read_csv(r'originalcsvs\karnataka_total_count.csv',index_col='year_month',parse_dates=True)        
        
    dfkarnataka.index.freq='MS'
    scaler.fit(dfkarnataka)
    scaled = scaler.transform(dfkarnataka)
    test_predictions = []

    n_input = 12
    n_features = 1

    first_eval_batch = scaled[-n_input:]
    current_batch = first_eval_batch.reshape((1, n_input, n_features))

    for i in range(input_month):
    
        # get the prediction value for the first batch
        current_pred = model.predict(current_batch)[0]
        
        # append the prediction into the array
        test_predictions.append(current_pred) 
        
        # use the prediction to update the batch and remove the first value
        current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)
    
    future_dates = pd.date_range(start=dfkarnataka.index[-1], end=selected_date+relativedelta(months=1), freq='ME')[3:]
    
    true_predictions = scaler.inverse_transform(test_predictions)
    # Create a range of future dates for plotting
    true_predictions_map = dict()
    for i,j in zip(future_dates, true_predictions):
        formated_time = i.strftime("%Y-%m-%d")
        # get the month in words
        # month = i.strftime("%B")
        true_predictions_map[formated_time] = round(j[0])
    # Plotting

    true_predictions_df = pd.DataFrame(true_predictions_map.items(), columns=["Month", "Predicted Count"])
    # future_dates = future_dates[:-2]
    # Plotting past and predicted values
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dfkarnataka.index, dfkarnataka['count'], label='Past Values')
    ax.plot(future_dates, true_predictions, label='Predicted Values')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title('Past and Predicted Values')
    ax.legend()

    # Display the plot using Streamlit
    st.pyplot(fig)
    return true_predictions_df
    # input_month = int(input("Enter the number of months you want to predict: "))

# Function to load data and create a district to unit mapping
# def load_district_unit_map():
#     df = pd.read_csv("../../Predictive Crime Analytics/FIR_Details_Data.csv")  # Update the path to your CSV file
#     district_unit_map = df.groupby('District_Name')['UnitName'].unique().to_dict()
#     return district_unit_map
def load_district_unit_map():
    with open("images/DistrictUnits.json", "r") as file:  # Update the path to your JSON file
        district_unit_map = json.load(file)
    return district_unit_map

district_unit_map = load_district_unit_map()

# Sidebar for inputs
st.sidebar.title('Input Parameters')

# Select Type (State, District, Unit)
state = st.sidebar.radio('State', ['Karnataka'], key='select_state')

# List of all districts
districts = ["ALL"] + list(district_unit_map.keys())
selected_district = st.sidebar.selectbox("District", districts, key='select_district')

# Update units based on selected district
units = ["ALL"] + district_unit_map.get(selected_district, [])
selected_unit = st.sidebar.selectbox("Unit", units, key='select_unit')

# Future Date Input
today = datetime.today()
min_date = today + relativedelta(days=1)  # Ensure only future dates can be selected
selected_date = st.sidebar.date_input("Seasonal Prediction", value=min_date, min_value=min_date, key='select_future_date')

# Calculate the number of months from the current month
if selected_date:
    months_diff = (selected_date.year - today.year) * 12 + selected_date.month - today.month

# Type of Crime Input
crime_types = ['ALL', 'POCSO', 'KARNATAKA POLICE ACT 1963', 'MOTOR VEHICLE ACCIDENTS NON-FATAL', 'MOTOR VEHICLE ACCIDENTS FATAL', 'THEFT', 'CrPC', 'CRUELTY BY HUSBAND', 'ATTEMPT TO MURDER', 'CHEATING', 'Karnataka State Local Act', 'ELECTION', 'REPRESENTATION OF PEOPLE ACT 1951 & 1988', 'MOLESTATION', 'MISSING PERSON', 'CASES OF HURT', 'FORGERY', 'SCHEDULED CASTE AND THE SCHEDULED TRIBES', 'BURGLARY - NIGHT', 'NEGLIGENT ACT', 'MURDER', 'RIOTS', 'Attempting to commit offences', 'KIDNAPPING AND ABDUCTION', 'EXPLOSIVES', 'EXPOSURE AND ABANDONMENT OF CHILD', 'ARSON', 'CONSUMER', 'OFFENCES AGAINST PUBLIC SERVANTS (Public servant is a victim)', 'CRIMES RELATED TO WOMEN', 'DEATHS DUE TO RASHNESS/NEGLIGENCE', 'COMMUNAL / RELIGION', 'DOWRY DEATHS', 'CRIMINAL BREACH OF TRUST', 'DACOITY', 'PREVENTION OF DAMAGE TO PUBLIC PROPERTY ACT 1984', 'BURGLARY - DAY', 'ANIMAL', 'MISCHIEF', 'INSULTING MODESTY OF WOMEN (EVE TEASING)', 'CRIMINAL TRESPASS', 'CRIMINAL INTIMIDATION', 'CRIMINAL CONSPIRACY', 'SUICIDE', 'NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES', 'PUBLIC SAFETY', 'CHILDREN ACT', 'ROBBERY', 'RAPE', 'ANTIQUES (CULTURAL PROPERTY)', 'CYBER CRIME', 'Concealment of birth by secret disposal of Child', 'FOREST', 'AFFRAY', 'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 'DEFAMATION', 'ATTEMPT TO CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 'WRONGFUL RESTRAINT/CONFINEMENT', 'COTPA, CIGARETTES AND OTHER TOBACCO PRODUCTS', 'CRIMINAL MISAPPROPRIATION', 'ASSAULT OR USE OF CRIMINAL FORCE TO DISROBE WOMAN', 'Disobedience to Order Promulgated by PublicServan', 'UNNATURAL SEX', 'POISONING-PROFESSIONAL', 'ASSAULT', 'ARMS ACT 1959', 'SEDITION', 'COPY RIGHT ACT 1957', 'OF ABETMENT', 'OFFENCES RELATED TO MARRIAGE', 'PUBLIC NUISANCE', 'Failure to appear to Court', 'ADULTERATION', 'POST & TELEGRAPH, TELEGRAPH WIRES(UNLAWFUL POSSESSION)ACT 1950', 'IMPERSONATION', 'PUBLIC JUSTICE', 'OFFENCES PROMOTING ENEMITY', 'INDIAN MOTOR VEHICLE', 'COUNTERFEITING', 'DEATHS-MISCARRIAGE', 'PORNOGRAPHY', 'IMMORAL TRAFFIC', 'FALSE EVIDENCE', 'BONDED LABOUR SYSTEM', 'ESCAPE FROM LAWFUL CUSTODY AND RESISTANCE', 'PASSPORT ACT', 'Human Trafficking', 'OFFENCES BY PUBLIC SERVANTS (EXCEPT CORRUPTION) (Public servant is accused)', 'SLAVERY', 'Giving false information respecting an offence com', 'FOREIGNER', 'RECEIVING OF STOLEN PROPERTY', 'OFFICIAL SECURITY RELATED ACTS', 'UNLAWFUL ACTIVITIES(Prevention)ACT 1967', 'UNNATURAL DEATH (Sec 174/174c/176)', 'CINEMATOGRAPH ACT 1952', 'DOCUMENTS & PROPERTY MARKS', 'DEFENCE FORCES OFFENCES RELATING TO (also relating to desertion)', 'INDIAN ELECTRICITY ACT', 'PREVENTION OF CORRUPTION ACT 1988', 'INFANTICIDE', 'NATIONAL SECURITY ACT', 'ILLEGAL DETENTION', 'RAILWAYS ACT', 'OFFENCES AGAINST STATE', 'CIVIL RIGHTS', 'FAILURE TO APPEAR TO COURT', 'BUYING & SELLING MINOR FOR PROSTITUTION']  # Complete with your list of crime types
selected_crime = st.sidebar.selectbox("Type of Crime", crime_types, key='select_crime_type')

# Main page to display inputs confirmation
st.title("Future Crime Prediction")
st.write("Selected District:", selected_district)
st.write("Selected Unit:", selected_unit)
if selected_date:
    st.write("Selected Future Date:", selected_date)
    st.write("Months from current month:", months_diff)
st.write("Selected Type of Crime:", selected_crime)

# Button to trigger prediction
if st.button("Run Prediction"):
    # Here you will call your model prediction function
    true_mp = predict_crime(selected_unit,selected_crime,selected_district,months_diff,selected_date)
    st.table(true_mp)