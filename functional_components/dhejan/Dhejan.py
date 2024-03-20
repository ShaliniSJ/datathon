import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import numpy as np

# Load district coordinates from JSON file and cache the data
@st.cache_data()
def load_district_coordinates(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return {district: (info["lat"], info["lon"]) for district, info in data.items()}

# Generate color codes and cache the colors
@st.cache_data()
def generate_color():
    np.random.seed(42)  # Seed for reproducibility
    return [np.random.randint(0, 255) for _ in range(3)] + [200]  # RGBA format

# Load CSV file with district names and cache the data
@st.cache_resource
def load_district_names(csv_file):
    df = pd.read_csv(csv_file)
    return df["District_Name"].unique().tolist()

def mapping_demo(csv_file, json_file):
    # Load district names
    districts_to_visualize = load_district_names(csv_file)

    # Load district coordinates
    districts_coordinates = load_district_coordinates(json_file)

    # Generate color codes
    district_colors = generate_color()

    data = pd.DataFrame({
        "District": districts_to_visualize,
        "Color": [district_colors[i % len(district_colors)] for i in range(len(districts_to_visualize))]
    })

    selected_district = st.selectbox("Select a district to view numbers", districts_to_visualize)

    if selected_district:
        st.write(f"Selected District: {selected_district}")
        st.write(f"Latitude: {districts_coordinates[selected_district][0]}")
        st.write(f"Longitude: {districts_coordinates[selected_district][1]}")

        # Create a separate DataFrame for the highlight layer
        highlight_data = data[data["District"] == selected_district]

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": districts_coordinates[selected_district][0],
                    "longitude": districts_coordinates[selected_district][1],
                    "zoom": 8,  # Zoom level for selected district
                    "pitch": 0,
                },
                layers=[
                    pdk.Layer(
                        "TextLayer",
                        data=data,
                        get_position=["lon", "lat"],
                        get_text="District",
                        get_color="Color",
                        get_size=12,  # Reduced font size
                        get_alignment_baseline="'bottom'",
                        pickable=True,
                        auto_highlight=True,
                    ),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=highlight_data,
                        get_position=["lon", "lat"],
                        get_radius=20000,  # Adjust the radius for highlighting
                        get_fill_color=[255, 0, 0, 150],  # Highlight color with reduced transparency
                        pickable=True,
                    ),
                ],
            )
        )

st.set_page_config(page_title="Karnataka Districts Map", page_icon="🗺️")
st.markdown("# Karnataka Districts Map")
st.sidebar.header("Karnataka Districts Map")

csv_file = r"C:\\Users\\Legion\Desktop\\KSP DATATHON\\datathon\\functional_components\\Predictive Crime Analytics\\AccusedData.csv"
json_file = "district_coordinates.json"
mapping_demo(csv_file, json_file)
