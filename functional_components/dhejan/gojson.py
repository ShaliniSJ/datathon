import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Load accused data from CSV file
accused_data = pd.read_csv(r"C:\\Users\\Legion\\Desktop\\KSP DATATHON\\datathon\\functional_components\\Predictive Crime Analytics\\AccusedData.csv")

# Load Karnataka GeoJSON file for district coordinates
with open(r"C:\\Users\\Legion\\Desktop\\KSP DATATHON\datathon\\functional_components\\images\\karnataka.json", 'r') as f:
    karnataka_geojson = json.load(f)

# Extract district coordinates from GeoJSON file
karnataka_districts = {}
for feature in karnataka_geojson['features']:
    district_name = feature['properties']['district']
    coordinates = feature['geometry']['coordinates']
    if coordinates:
        if len(coordinates[0]) == 1:
            # For single coordinate, take the middle point
            latitude = coordinates[0][0][1]
            longitude = coordinates[0][0][0]
        else:
            # For multiple coordinates, take the average
            latitude = sum(coord[1] for coord in coordinates[0]) / len(coordinates[0])
            longitude = sum(coord[0] for coord in coordinates[0]) / len(coordinates[0])
        karnataka_districts[district_name] = (latitude, longitude)

# Filter relevant columns from accused data
accused_data_filtered = accused_data[["District_Name", "Year", "age", "Caste", "Profession", "Sex", "Month"]]

# Define function to apply filters and create heatmap based on selected filters
def create_heatmap(selected_lower_age, selected_upper_age, selected_sex, selected_month):
    # Apply filters
    filtered_data = accused_data_filtered[
        (accused_data_filtered["age"] >= selected_lower_age) &
        (accused_data_filtered["age"] <= selected_upper_age) &
        (accused_data_filtered["Sex"] == selected_sex) &
        (accused_data_filtered["Month"] == selected_month)
    ]

    # Group data for visualization
    grouped_data = filtered_data.groupby(["District_Name"]).size().reset_index(name="AccusedCount")

    # Add latitude and longitude columns based on the Karnataka district coordinates
    grouped_data["latitude"] = grouped_data["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[0])
    grouped_data["longitude"] = grouped_data["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[1])

    # Define pydeck layers for visualization
    layers = [
        pdk.Layer(
            "HeatmapLayer",
            data=grouped_data,
            get_position=["longitude", "latitude"],
            aggregation='"MEAN"',
            get_weight="AccusedCount",
            radius=5000,
        ),
        pdk.Layer(
            "GeoJsonLayer",
            data=karnataka_geojson,
            filled=False,
            stroked=True,
            lineWidthMinPixels=2,
            get_line_color=[255, 0, 0],
        )
    ]

    # Display the map with selected filters
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": 14.5204, "longitude": 75.7224, "zoom": 7, "pitch": 50},
            layers=layers,
        )
    )

# Display the filters and create heatmap based on selected filters
st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
st.markdown("# Accused Heatmap Demo")
st.sidebar.header("Accused Heatmap Filters")

# Define filter options
sex_options = accused_data_filtered["Sex"].unique().tolist()
month_options = accused_data_filtered["Month"].unique().tolist()

# Add filter widgets
selected_lower_age = st.sidebar.number_input("Lower Age Limit:", min_value=0, max_value=120, step=1, value=0)
selected_upper_age = st.sidebar.number_input("Upper Age Limit:", min_value=0, max_value=120, step=1, value=120)
selected_sex = st.sidebar.selectbox("Select Sex:", sex_options)
selected_month = st.sidebar.selectbox("Select Month:", month_options)

# Display heatmap based on selected filters
create_heatmap(selected_lower_age, selected_upper_age, selected_sex, selected_month)
