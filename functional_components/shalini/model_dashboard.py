import streamlit as st
from datetime import datetime

# Sidebar for inputs
st.sidebar.title('Input Parameters')

# Title Input
title = st.sidebar.text_input('Title', 'Default Title')

# Select Type (State, District, Unit)
state = st.sidebar.selectbox('State', ['Karnataka'], key='select_state')
districts = ['ALL', 'Bagalkot', 'Ballari', 'Belagavi City', 'Belagavi Dist', 'Bengaluru City', 'Bengaluru Dist', 'Bidar', 'Chamarajanagar', 'Chickballapura', 'Chikkamagaluru', 'Chitradurga', 'CID', 'Coastal Security Police', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Hubballi Dharwad City', 'ISD Bengaluru', 'K.G.F', 'Kalaburagi', 'Kalaburagi City', 'Karnataka Railways', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mangaluru City', 'Mysuru City', 'Mysuru Dist', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayanagara', 'Vijayapur', 'Yadgir']
units = ['Unit1', 'Unit2']  # Example units

selected_type = st.sidebar.radio("Select Type", ("State", "District", "Unit"), key='select_type')
if selected_type == "State":
    selected_state = st.sidebar.selectbox("State", [state], key='select_state_inner')
elif selected_type == "District":
    selected_district = st.sidebar.selectbox("District", districts, key='select_district')
else:
    selected_unit = st.sidebar.selectbox("Unit", units, key='select_unit')

# Date Range Input
date_selection = st.sidebar.date_input("Date Range", [], key='select_date_range')
start_date, end_date = None, None
if isinstance(date_selection, tuple) and len(date_selection) == 2:
    start_date, end_date = date_selection

# Type of Crime Input
crime_types = ['ALL', 'POCSO', 'KARNATAKA POLICE ACT 1963', ...]
selected_crime = st.sidebar.selectbox("Type of Crime", crime_types, key='select_crime_type')

# Main page to display title and inputs confirmation
st.title(title)
st.write("Selected State:", state)
if selected_type == "District":
    st.write("Selected District:", selected_district)
elif selected_type == "Unit":
    st.write("Selected Unit:", selected_unit)
if start_date and end_date:
    st.write("Selected Date Range:", start_date, 'to', end_date)
else:
    st.write("Date Range not selected.")
st.write("Selected Type of Crime:", selected_crime)

# Button to trigger prediction
if st.button("Run Prediction"):
    # Here you will call your model prediction function
    st.write("Prediction process would be here.")
