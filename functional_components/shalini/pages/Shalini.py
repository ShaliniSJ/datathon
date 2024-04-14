import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import matplotlib.pyplot as plt

# Initialize tab_name in session_state
if "tab_name" not in st.session_state:
    st.session_state.tab_name = "State View"

# Load accused data from Parquet file
accused_data = pd.read_csv(r"../../Predictive Crime Analytics/AccusedData.csv")

# Load Karnataka GeoJSON file for district coordinates
with open(r"../images/karnataka.json", "r") as f:
    karnataka_geojson = json.load(f)

# Load district units from JSON file
with open(r"../images/district_units.json", "r") as f:
    district_units_data = json.load(f)

# Extract district coordinates from GeoJSON file
karnataka_districts = {}
for feature in karnataka_geojson["features"]:
    district_name = feature["properties"]["district"]
    coordinates = feature["geometry"]["coordinates"]
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
accused_data_filtered = accused_data[
    ["District_Name", "Year", "age", "Caste", "Profession", "Sex", "Month"]
]

# Define district_layer before using it
district_layer = pdk.Layer(
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
)


# Function to create a visualization based on selected filters
def create_heatmap(
    selected_age, selected_sex, selected_year, selected_month, selected_district=None
):
    # Convert selected_year to a list
    selected_year_list = [selected_year]

    # Apply filters
    filtered_data = accused_data_filtered[
        (accused_data_filtered["age"].between(selected_age[0], selected_age[1]))
        & (accused_data_filtered["Sex"].isin(selected_sex))
        & (accused_data_filtered["Year"].isin(selected_year_list))
        & (accused_data_filtered["Month"] == selected_month)
    ]

    # Group data for visualization
    grouped_data = (
        filtered_data.groupby(["District_Name"]).size().reset_index(name="AccusedCount")
    )

    # Add latitude and longitude columns based on the Karnataka district coordinates
    grouped_data["latitude"] = grouped_data["District_Name"].map(
        lambda x: karnataka_districts.get(x, (None, None))[0]
    )
    grouped_data["longitude"] = grouped_data["District_Name"].map(
        lambda x: karnataka_districts.get(x, (None, None))[1]
    )

    return grouped_data


# Display the app
st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
st.title("KSP Crime Analytics")

# Use expander for tabs
with st.expander("State View", expanded=st.session_state.tab_name == "State View"):
    st.session_state.tab_name = "State View"
    st.header("State View")

    # Sidebar UI for filter selection
    selected_age_state = st.slider(
        "Select Age Limit (State)", 0, 120, (0, 120), key="age_slider_state"
    )
    selected_sex_state = []
    if st.checkbox("Male (State)", True, key="male_checkbox_state"):
        selected_sex_state.append("MALE")
    if st.checkbox("Female (State)", True, key="female_checkbox_state"):
        selected_sex_state.append("FEMALE")
    selected_year_state = st.slider(
        "Select Year (State)", 2016, 2024, 2016, key="year_slider_state"
    )
    selected_month_state = st.slider(
        "Select Month (State)", 1, 12, 1, key="month_slider_state"
    )

    # Call create_heatmap with user selected inputs and get the DataFrame object
    heatmap_data = create_heatmap(
        selected_age_state,
        selected_sex_state,
        selected_year_state,
        selected_month_state,
        [],
    )
    if not heatmap_data.empty:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 14.5204,
                    "longitude": 75.7224,
                    "zoom": 6,
                    "pitch": 50,
                },
                layers=[
                    pdk.Layer(
                        "HeatmapLayer",
                        data=heatmap_data,
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
                    # Add district borders layer
                    district_layer,
                ],
            )
        )
        legend_handles = [
            plt.Line2D(
                [0],
                [0],
                marker="s",
                color="w",
                label="0-50",
                markerfacecolor="red",
                markersize=10,
            ),
            plt.Line2D(
                [0],
                [0],
                marker="s",
                color="w",
                label="51-100",
                markerfacecolor="yellow",
                markersize=10,
            ),
            plt.Line2D(
                [0],
                [0],
                marker="s",
                color="w",
                label="101-150",
                markerfacecolor="green",
                markersize=10,
            ),
            # Add more legend entries as needed
        ]

    else:
        st.warning("No data available for the selected filters.")

with st.expander(
    "District View", expanded=st.session_state.tab_name == "District View"
):
    st.session_state.tab_name = "District View"
    st.header("District View")

    # Function to get unit names based on selected district
    def get_unit_names(selected_district):
        unit_names_data = district_units_data.get(selected_district, [])
        if isinstance(unit_names_data, list):
            return unit_names_data
        else:
            return (
                []
            )  # Return an empty list or handle the case based on your application's logic

    # Sidebar UI for filter selection
    selected_district = st.selectbox(
        "Select District", sorted(karnataka_districts.keys()), key="district_select"
    )
    selected_unit = st.selectbox(
        "Select Unit Name", get_unit_names(selected_district), key="unit_select"
    )
    selected_age_district = st.slider(
        "Select Age Limit (district)", 0, 120, (0, 120), key="age_slider_district"
    )
    selected_sex_district = []
    if st.checkbox("Male (district)", True, key="male_checkbox_district"):
        selected_sex_district.append("MALE")
    if st.checkbox("Female (district)", True, key="female_checkbox_district"):
        selected_sex_district.append("FEMALE")
        selected_year_district = st.slider(
            "Select Year (district)", 2016, 2024, 2016, key="year_slider_district"
        )
        selected_month_district = st.slider(
            "Select Month (district)", 1, 12, 1, key="month_slider_district"
        )

        # Zoom to the selected district on the map
        district_coordinates = karnataka_districts.get(selected_district, None)
        if district_coordinates:
            latitude, longitude = district_coordinates
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": latitude,
                        "longitude": longitude,
                        "zoom": 8,  # Adjust the zoom level as needed
                        "pitch": 50,
                    },
                    layers=[district_layer],
                )
            )
        else:
            st.warning("Coordinates not found for the selected district.")
