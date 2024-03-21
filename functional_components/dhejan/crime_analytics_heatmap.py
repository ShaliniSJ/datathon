import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Load accused data from Parquet file
accused_data = pd.read_csv(r"../../Predictive Crime Analytics/AccusedData.csv")

# Load Karnataka GeoJSON file for district coordinates
with open(r"../images/karnataka.json", 'r') as f:
    karnataka_geojson = json.load(f)

# Load police station data (units and their coordinates) from JSON file
with open(r"../images/structured_police_stations.json", 'r') as f:
    police_station_data = json.load(f)

# Function to get police station coordinates in the selected district
def get_police_station_coordinates(district):
    return police_station_data.get(district, {})

# Extract district coordinates from GeoJSON file for the initial map view
karnataka_districts = {}
for feature in karnataka_geojson['features']:
    district_name = feature['properties']['district']
    coordinates = feature['geometry']['coordinates']
    if coordinates:
        if len(coordinates[0]) == 1:
            latitude = coordinates[0][0][1]
            longitude = coordinates[0][0][0]
        else:
            latitude = sum(coord[1] for coord in coordinates[0]) / len(coordinates[0])
            longitude = sum(coord[0] for coord in coordinates[0]) / len(coordinates[0])
        karnataka_districts[district_name] = (latitude, longitude)

# Function to create a heatmap for police stations in the selected district
def create_police_station_heatmap(selected_district, selected_age, selected_sex, selected_year, selected_month):
    police_stations = get_police_station_coordinates(selected_district)
    filtered_data = accused_data[
        (accused_data["age"].between(selected_age[0], selected_age[1])) &
        (accused_data["Sex"].isin(selected_sex)) &
        (accused_data["Year"] == selected_year) &
        (accused_data["Month"] == selected_month) &
        (accused_data["UnitName"].isin(police_stations.keys()))
    ]

    # Group data by UnitName and count the occurrences
    grouped_data = filtered_data.groupby(["UnitName"]).size().reset_index(name="AccusedCount")

    # Add latitude and longitude columns for each police station
    grouped_data["latitude"] = grouped_data["UnitName"].apply(lambda x: float(police_stations[x][0].split(',')[0]))
    grouped_data["longitude"] = grouped_data["UnitName"].apply(lambda x: float(police_stations[x][0].split(',')[1]))

    return grouped_data

# Streamlit UI for selecting filters and displaying the heatmap
st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
st.title("KSP Crime Analytics")

selected_district = st.selectbox("Select District", sorted(karnataka_districts.keys()))
selected_age = st.slider("Select Age Limit", 0, 120, (0, 120))
selected_sex = st.multiselect("Select Gender", ["MALE", "FEMALE"], default=["MALE", "FEMALE"])
selected_year = st.slider("Select Year", 2016, 2024, 2016)
selected_month = st.slider("Select Month", 1, 12, 1)

heatmap_data = create_police_station_heatmap(selected_district, selected_age, selected_sex, selected_year, selected_month)
if not heatmap_data.empty:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": karnataka_districts[selected_district][0],
                "longitude": karnataka_districts[selected_district][1],
                "zoom": 11,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HeatmapLayer",
                    data=heatmap_data,
                    get_position=["longitude", "latitude"],
                    aggregation='"MEAN"',
                    get_weight="AccusedCount",
                    radius=100,
                    color_range=[
                        [255, 0, 0, 255],
                        [255, 165, 0, 255],
                        [255, 255, 0, 255],
                        [0, 128, 0, 255],
                        [0, 0, 255, 255]
                    ],
                )
            ],
        )
    )
else:
    st.warning("No data available for the selected filters.")
