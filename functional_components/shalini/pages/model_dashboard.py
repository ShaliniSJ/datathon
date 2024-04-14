import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Function to load data and create a district to unit mapping
def load_district_unit_map():
    df = pd.read_csv("../../../Predictive Crime Analytics/FIR_Details_Data.csv")  # Update the path to your CSV file
    district_unit_map = df.groupby('District_Name')['UnitName'].unique().to_dict()
    return district_unit_map

district_unit_map = load_district_unit_map()

# Sidebar for inputs
st.sidebar.title('Input Parameters')

# Select Type (State, District, Unit)
state = st.sidebar.radio('State', ['Karnataka'], key='select_state')

# List of all districts
districts = list(district_unit_map.keys())
selected_district = st.sidebar.selectbox("District", districts, key='select_district')

# Update units based on selected district
units = district_unit_map.get(selected_district, [])
selected_unit = st.sidebar.selectbox("Unit", units, key='select_unit')

# Future Date Input
today = datetime.today()
min_date = today + relativedelta(days=1)  # Ensure only future dates can be selected
selected_date = st.sidebar.date_input("Select Future Date", value=min_date, min_value=min_date, key='select_future_date')

# Calculate the number of months from the current month
if selected_date:
    months_diff = (selected_date.year - today.year) * 12 + selected_date.month - today.month

# Type of Crime Input
crime_types = ['ALL', 'POCSO', 'KARNATAKA POLICE ACT 1963', 'MOTOR VEHICLE ACCIDENTS NON-FATAL', 'MOTOR VEHICLE ACCIDENTS FATAL', 'THEFT', 'CrPC', 'CRUELTY BY HUSBAND', 'ATTEMPT TO MURDER', 'CHEATING', 'Karnataka State Local Act', 'ELECTION', 'REPRESENTATION OF PEOPLE ACT 1951 & 1988', 'MOLESTATION', 'MISSING PERSON', 'CASES OF HURT', 'FORGERY', 'SCHEDULED CASTE AND THE SCHEDULED TRIBES', 'BURGLARY - NIGHT', 'NEGLIGENT ACT', 'MURDER', 'RIOTS', 'Attempting to commit offences', 'KIDNAPPING AND ABDUCTION', 'EXPLOSIVES', 'EXPOSURE AND ABANDONMENT OF CHILD', 'ARSON', 'CONSUMER', 'OFFENCES AGAINST PUBLIC SERVANTS (Public servant is a victim)', 'CRIMES RELATED TO WOMEN', 'DEATHS DUE TO RASHNESS/NEGLIGENCE', 'COMMUNAL / RELIGION', 'DOWRY DEATHS', 'CRIMINAL BREACH OF TRUST', 'DACOITY', 'PREVENTION OF DAMAGE TO PUBLIC PROPERTY ACT 1984', 'BURGLARY - DAY', 'ANIMAL', 'MISCHIEF', 'INSULTING MODESTY OF WOMEN (EVE TEASING)', 'CRIMINAL TRESPASS', 'CRIMINAL INTIMIDATION', 'CRIMINAL CONSPIRACY', 'SUICIDE', 'NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES', 'PUBLIC SAFETY', 'CHILDREN ACT', 'ROBBERY', 'RAPE', 'ANTIQUES (CULTURAL PROPERTY)', 'CYBER CRIME', 'Concealment of birth by secret disposal of Child', 'FOREST', 'AFFRAY', 'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 'DEFAMATION', 'ATTEMPT TO CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 'WRONGFUL RESTRAINT/CONFINEMENT', 'COTPA, CIGARETTES AND OTHER TOBACCO PRODUCTS', 'CRIMINAL MISAPPROPRIATION', 'ASSAULT OR USE OF CRIMINAL FORCE TO DISROBE WOMAN', 'Disobedience to Order Promulgated by PublicServan', 'UNNATURAL SEX', 'POISONING-PROFESSIONAL', 'ASSAULT', 'ARMS ACT 1959', 'SEDITION', 'COPY RIGHT ACT 1957', 'OF ABETMENT', 'OFFENCES RELATED TO MARRIAGE', 'PUBLIC NUISANCE', 'Failure to appear to Court', 'ADULTERATION', 'POST & TELEGRAPH, TELEGRAPH WIRES(UNLAWFUL POSSESSION)ACT 1950', 'IMPERSONATION', 'PUBLIC JUSTICE', 'OFFENCES PROMOTING ENEMITY', 'INDIAN MOTOR VEHICLE', 'COUNTERFEITING', 'DEATHS-MISCARRIAGE', 'PORNOGRAPHY', 'IMMORAL TRAFFIC', 'FALSE EVIDENCE', 'BONDED LABOUR SYSTEM', 'ESCAPE FROM LAWFUL CUSTODY AND RESISTANCE', 'PASSPORT ACT', 'Human Trafficking', 'OFFENCES BY PUBLIC SERVANTS (EXCEPT CORRUPTION) (Public servant is accused)', 'SLAVERY', 'Giving false information respecting an offence com', 'FOREIGNER', 'RECEIVING OF STOLEN PROPERTY', 'OFFICIAL SECURITY RELATED ACTS', 'UNLAWFUL ACTIVITIES(Prevention)ACT 1967', 'UNNATURAL DEATH (Sec 174/174c/176)', 'CINEMATOGRAPH ACT 1952', 'DOCUMENTS & PROPERTY MARKS', 'DEFENCE FORCES OFFENCES RELATING TO (also relating to desertion)', 'INDIAN ELECTRICITY ACT', 'PREVENTION OF CORRUPTION ACT 1988', 'INFANTICIDE', 'NATIONAL SECURITY ACT', 'ILLEGAL DETENTION', 'RAILWAYS ACT', 'OFFENCES AGAINST STATE', 'CIVIL RIGHTS', 'FAILURE TO APPEAR TO COURT', 'BUYING & SELLING MINOR FOR PROSTITUTION']  # Complete with your list of crime types
selected_crime = st.sidebar.selectbox("Type of Crime", crime_types, key='select_crime_type')

# Main page to display inputs confirmation
st.title("MODEL PREDICTION")
st.write("Selected District:", selected_district)
st.write("Selected Unit:", selected_unit)
if selected_date:
    st.write("Selected Future Date:", selected_date)
    st.write("Months from current month:", months_diff)
st.write("Selected Type of Crime:", selected_crime)

# Button to trigger prediction
if st.button("Run Prediction"):
    # Here you will call your model prediction function
    st.write("Prediction process would be here.")
