import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Load accused data from Parquet file
accused_data = pd.read_csv(r"Predictive Crime Analytics\AccusedData.csv")

# Load Karnataka GeoJSON file for district coordinates
with open(r"functional_components\images\karnataka.json", 'r') as f:
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
def create_heatmap(selected_age, selected_sex, selected_year, selected_month, selected_layers):
    # Convert selected_year to a list
    selected_year_list = [selected_year]

    # Apply filters
    filtered_data = accused_data_filtered[
        (accused_data_filtered["age"].between(selected_age[0], selected_age[1])) &
        (accused_data_filtered["Sex"].isin(selected_sex)) &
        (accused_data_filtered["Year"].isin(selected_year_list)) &
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
            color_range=[
                [255, 0, 0, 255],
                [255, 165, 0, 255],
                [255, 255, 0, 255],
                [0, 128, 0, 255],
                [0, 0, 255, 255],
            ],
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
            get_line_color=[0, 0, 0],
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
        if st.sidebar.checkbox(layer_name, True, key=f"{layer_name}_checkbox_{tab_name}")
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 14.5204,
                    "longitude": 75.7224,
                    "zoom": 6,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")

# Display the app
st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
st.title("KSP Crime Analytics")

# Create two tabs for State View and District View
tab_name = st.radio("Select View", ["State View", "District View"])

# Content based on selected tab
if tab_name == "State View":
    st.header("State View")
    
    # Sidebar UI for filter selection
    selected_age_state = st.slider("Select Age Limit (State)", 0, 120, (0, 120), key="age_slider_state")
    selected_sex_state = []
    if st.checkbox("Male (State)", True, key="male_checkbox_state"):
        selected_sex_state.append("MALE")
    if st.checkbox("Female (State)", True, key="female_checkbox_state"):
        selected_sex_state.append("FEMALE")
    selected_year_state = st.slider("Select Year (State)", 2016, 2024, 2016, key="year_slider_state")
    selected_month_state = st.slider("Select Month (State)", 1, 12, 1, key="month_slider_state")

    # Call create_heatmap with user selected inputs
    create_heatmap(selected_age_state, selected_sex_state, selected_year_state, selected_month_state, [])

else:
    st.header("District View")
    
    selected_age_district = st.slider("Select Age Limit (District)", 0, 120, (0, 120), key="age_slider_district")
    selected_sex_district = []
    if st.checkbox("Male (District)", True, key="male_checkbox_district"):
        selected_sex_district.append("MALE")
    if st.checkbox("Female (District)", True, key="female_checkbox_district"):
        selected_sex_district.append("FEMALE")
    selected_year_district = st.slider("Select Year (District)", 2016, 2024, 2016, key="year_slider_district")
    selected_month_district = st.slider("Select Month (District)", 1, 12, 1, key="month_slider_district")

    # Call create_heatmap with user selected inputs
    create_heatmap(selected_age_district, selected_sex_district, selected_year_district, selected_month_district, [])
