import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Load accused data from Parquet file
accused_data=pd.read_parquet(r"../../Predictive Crime Analytics/AccusedData.parquet")

# Load Karnataka GeoJSON file for district coordinates
with open(r"../images/karnataka.json", 'r') as f:
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

# Function to create a visualization based on selected filters
def create_heatmap(selected_age, selected_sex, selected_month, selected_layers):
    # Apply filters
    filtered_data = accused_data_filtered[
        (accused_data_filtered["age"].between(selected_age[0], selected_age[1])) &
        (accused_data_filtered["Sex"].isin(selected_sex)) &
        (accused_data_filtered["Month"] == selected_month)
    ]

    # Group data for visualization
    grouped_data = filtered_data.groupby(["District_Name"]).size().reset_index(name="AccusedCount")

    # Add latitude and longitude columns based on the Karnataka district coordinates
    grouped_data["latitude"] = grouped_data["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[0])
    grouped_data["longitude"] = grouped_data["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[1])

    # Define pydeck layers for visualization
    ALL_LAYERS = {
        "Heatmap": pdk.Layer(
            "HeatmapLayer",
            data=grouped_data,
            get_position=["longitude", "latitude"],
            aggregation='"MEAN"',
            get_weight="AccusedCount",
            radius=5000,
        ),
        "Hexagon": pdk.Layer(
            "HexagonLayer",
            data=grouped_data,
            get_position=["longitude", "latitude"],
            auto_highlight=True,
            radius=5000,
            elevation_scale=50,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "District Borders": pdk.Layer(
            "GeoJsonLayer",
            data=karnataka_geojson,
            filled=False,
            stroked=True,
            lineWidthMinPixels=2,
            get_line_color=[255, 0, 0],
            get_text="properties.district",
            get_text_color=[0, 255, 0],  # Green color for district names
            get_text_size=20,
            get_text_anchor="middle",
        ),
    }

    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/dark-v9",
                initial_view_state={
                    "latitude": 14.5204,
                    "longitude": 75.7224,
                    "zoom": 7,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")

# Display the app
st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
st.markdown("# Accused Mapping Demo")
st.sidebar.header("Accused Filters")

# Sidebar UI for filter selection
selected_age = st.sidebar.slider("Select Age Limit", 0, 120, (0, 120), key="sidebar_age_slider")
selected_sex = []
if st.sidebar.checkbox("Male", True, key="sidebar_male_checkbox"):
    selected_sex.append("MALE")
if st.sidebar.checkbox("Female", True, key="sidebar_female_checkbox"):
    selected_sex.append("FEMALE")
selected_month = st.sidebar.slider("Select Month", 1, 12, 1, key="sidebar_month_slider")

# Call create_heatmap with user selected inputs
create_heatmap(selected_age, selected_sex, selected_month, [])
