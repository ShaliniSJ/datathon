import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import plotly.express as px
from io import BytesIO
import base64

# Helper functions
def get_table_download_link(df):
    """Generates a download link allowing the data in a given panda dataframe to be downloaded as a csv"""
    towrite = BytesIO()
    df.to_csv(towrite, encoding='utf-8', index=False)
    towrite.seek(0)  # rewind the buffer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    return f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download CSV file</a>'

def load_data(file_path):
    """Load data from CSV file."""
    return pd.read_csv(file_path)

def load_unit_data(json_path):
    """Load unit data from a JSON file."""
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data
# Load data
file_path = "../../Predictive Crime Analytics/FIR_Details_Data.csv"
json_path = "images/district_units.json"
df_fir = load_data(file_path)
unit_data = load_unit_data(json_path)
df_fir = df_fir.drop(columns=['io assigned', 'conviction head count'], errors='ignore')

# Streamlit layout setup
st.title('Crime Data Visualization Tool')
st.sidebar.title('Filters')
st.sidebar.markdown('## Filter FIR Data')

# FIR Type and Crime Types filter setup
selected_fir_type = st.sidebar.radio('Select FIR Type:', ['All', 'Heinous', 'Non-Heinous'], index=0)
selected_crime_types = st.sidebar.multiselect('Crime Types', df_fir['CrimeGroup_Name'].unique(), default=df_fir['CrimeGroup_Name'].unique())
if selected_fir_type != 'All':
    df_fir = df_fir[df_fir['FIR Type'] == selected_fir_type]
filtered_df = df_fir[df_fir['CrimeGroup_Name'].isin(selected_crime_types)] if selected_crime_types else df_fir

# District and Unit selection
selected_district = st.sidebar.selectbox('Select District:', ['All'] + sorted(filtered_df['District_Name'].unique()))
if selected_district != 'All':
    filtered_df = filtered_df[filtered_df['District_Name'] == selected_district]
units_options = unit_data.get(selected_district, ['All']) if selected_district != 'All' else ['All']
selected_unit = st.sidebar.selectbox('Select Unit:', ['All'] + units_options)
if selected_unit != 'All':
    filtered_df = filtered_df[filtered_df['UnitName'] == selected_unit]

# Reset and export buttons
if st.sidebar.button('Reset Filters'):
    st.experimental_rerun()
if not filtered_df.empty:
    st.markdown(get_table_download_link(filtered_df), unsafe_allow_html=True)

# Heatmap visualization
st.header('Heatmap of FIR Incidents Based on Selected Filters')
layer = pdk.Layer(
    'HeatmapLayer',
    data=filtered_df.groupby(['Latitude', 'Longitude']).size().reset_index(name='Counts'),
    get_position='[Longitude, Latitude]',
    get_weight='Counts',
    radius_pixels=30,
    opacity=0.9,
    color_range=[[148, 0, 211], [75, 0, 130], [0, 0, 255], [0, 255, 0], [255, 255, 0], [255, 127, 0], [255, 0 , 0]]
)
view_state = pdk.ViewState(longitude=75.713888, latitude=15.317277, zoom=6)
r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style='mapbox://styles/mapbox/light-v9')
st.pydeck_chart(r)

# Data table display
st.header('Detailed FIR Data')
st.dataframe(filtered_df)

# Additional visualizations
if selected_district == 'All':
    st.header('Year-wise Crime Rate')
    crime_year_data = df_fir.groupby('Year').size().reset_index(name='Counts')
    fig_year = px.bar(crime_year_data, x='Year', y='Counts', title='Year-wise Crime Rate', color='Counts')
    st.plotly_chart(fig_year, use_container_width=True)
if selected_district != 'All':
    st.header(f'Crime Type Distribution in {selected_district}')
    crime_type_data = filtered_df['CrimeGroup_Name'].value_counts().reset_index()
    crime_type_data.columns = ['CrimeGroup_Name', 'Counts']

    # Pie chart with currently selected crime type highlighted
    fig_pie = px.pie(crime_type_data, values='Counts', names='CrimeGroup_Name', title=f'Crime Type Distribution in {selected_district}')
    if selected_crime_types:
        fig_pie.for_each_trace(lambda trace: trace.update(visible='legendonly') if trace.name not in selected_crime_types else ())
    st.plotly_chart(fig_pie, use_container_width=True)

# Display unit boundaries
if selected_unit != 'All':
    st.header(f'Unit Boundaries for {selected_unit}')
    unit_boundaries = unit_data.get(selected_unit)
    if unit_boundaries:
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            layers=[
                pdk.Layer(
                    'GeoJsonLayer',
                    data=unit_boundaries,
                    filled=False,
                    stroked=True,
                    get_line_color=[0, 0, 255],  # Blue color for unit boundaries
                    get_line_width=5,
                )
            ],
            initial_view_state={
                'latitude': 15.317277,
                'longitude': 75.713888,
                'zoom': 6,
                'pitch': 50,
            },
        ))

