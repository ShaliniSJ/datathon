import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Sidebar for inputs
st.sidebar.title('Input Parameters')

# Select Type (State, District, Unit)
state = st.sidebar.selectbox('State', ['Karnataka'], key='select_state')

# Mapping districts to specific units
district_unit_map = {
    'Bagalkot': ['Unit1', 'Unit2'],
    'Ballari': ['Unit3', 'Unit4'],
    'Belagavi City': ['Unit5', 'Unit6'],
    # Add more mappings here for each district
}

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
crime_types = ['ALL', 'POCSO', 'KARNATAKA POLICE ACT 1963', ...]  # Complete with your list of crime types
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
