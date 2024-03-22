import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Initialize tab_name in session_state
if "tab_name" not in st.session_state:
    st.session_state.tab_name = "State View"

# Load accused data from Parquet file
accused_data = pd.read_csv(r"../../Predictive Crime Analytics/AccusedData.csv")

# Load Karnataka GeoJSON file for district coordinates
with open(r"../images/karnataka.json", 'r') as f:
    karnataka_geojson = json.load(f)

# Load district units from JSON file
with open(r"../images/structured_police_stations.json", 'r') as f:
    unit_coordinates_data = json.load(f)

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
accused_data_filtered = accused_data[["District_Name", "UnitName", "Year", "age", "Caste", "Profession", "Sex", "Month"]]

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
def create_heatmap(selected_age, selected_sex, selected_year, selected_month, selected_district=None):
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

    return grouped_data

# Function to get unit coordinates based on selected district
def get_unit_coordinates(selected_district):
    unit_coordinates = unit_coordinates_data.get(selected_district, [])
    return unit_coordinates

# Display the app
st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
st.title("KSP Crime Analytics")

# Use expander for tabs
with st.expander("State View", expanded=st.session_state.tab_name == "State View"):
    st.session_state.tab_name = "State View"
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

    # Call create_heatmap with user selected inputs and get the DataFrame object
    heatmap_data = create_heatmap(selected_age_state, selected_sex_state, selected_year_state, selected_month_state, [])
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
    else:
        st.warning("No data available for the selected filters.")

with st.expander("District View", expanded=st.session_state.tab_name == "District View"):
    st.session_state.tab_name = "District View"
    st.header("District View")

    selected_district = st.selectbox("Select District", sorted(karnataka_districts.keys()), key="district_select")
    
    # Fetch unique professions and add "ALL" option
    unique_professions = accused_data['Profession'].unique().tolist()
    all_professions = ['ALL'] + unique_professions
    selected_profession = st.selectbox("Select Profession", all_professions, index=0, key="profession_select")

    selected_age_district = st.slider("Select Age Limit (district)", 0, 120, (0, 120), key="age_slider_district")
    selected_sex_district = st.multiselect("Select Gender (district)", ['MALE', 'FEMALE'], default=['MALE', 'FEMALE'], key="sex_multiselect_district")
    
    col_from_month, col_from_year, col_to_month, col_to_year = st.columns(4)
    with col_from_year:
        selected_from_year = st.number_input("From Year", min_value=2016, max_value=2024, value=2016, step=1, key="from_year")
    with col_to_year:
        selected_to_year = st.number_input("To Year", min_value=2016, max_value=2024, value=2024, step=1, key="to_year")
    with col_from_month:
        selected_from_month = st.number_input("From Month", min_value=1, max_value=12, value=1, step=1, key="from_month")
    with col_to_month:
        selected_to_month = st.number_input("To Month", min_value=1, max_value=12, value=12, step=1, key="to_month")
    
    def table_data(selected_district, selected_age, selected_sex, from_year, to_year, from_month, to_month):
        # Filter data based on the selected range of months and other filters
        filtered_data = accused_data[
            (accused_data["District_Name"] == selected_district) &
            (accused_data["age"].between(selected_age[0], selected_age[1])) &
            (accused_data["Sex"].isin(selected_sex)) &
            (accused_data["Year"].between(from_year, to_year)) &
            (accused_data["Month"].between(from_month, to_month))
        ]
        grouped_table_data = filtered_data.groupby("UnitName").agg(
            Male_Count=("Sex", lambda x: (x == "MALE").sum()),
            Female_Count=("Sex", lambda x: (x == "FEMALE").sum()),
            Average_Male_Age=("age", "mean"),
            Average_Female_Age=("age", "mean")
        ).reset_index()

        return grouped_table_data

    # Function to create a heatmap for units within the selected district
    def create_unit_heatmap(selected_district, selected_profession, selected_age, selected_sex, from_year, to_year, from_month, to_month):
        # Filter data based on the selected range of months and other filters
        if selected_profession == 'ALL':
            filtered_data = accused_data[
                (accused_data["District_Name"] == selected_district) &
                (accused_data["age"].between(selected_age[0], selected_age[1])) &
                (accused_data["Sex"].isin(selected_sex)) &
                (accused_data["Year"].between(from_year, to_year)) &
                (accused_data["Month"].between(from_month, to_month))
            ]
        else:
            filtered_data = accused_data[
                (accused_data["District_Name"] == selected_district) &
                (accused_data["Profession"] == selected_profession) &
                (accused_data["age"].between(selected_age[0], selected_age[1])) &
                (accused_data["Sex"].isin(selected_sex)) &
                (accused_data["Year"].between(from_year, to_year)) &
                (accused_data["Month"].between(from_month, to_month))
            ]
        units = get_unit_coordinates(selected_district)
        # Map each unit to its corresponding coordinate in the JSON file
        unit_locations = {
            unit: coordinates[0].split(', ') for unit, coordinates in units.items()
        }

        # Group the filtered data by UnitName
        grouped_data = filtered_data.groupby("UnitName").size().reset_index(name="AccusedCount")
        grouped_data["latitude"] = grouped_data["UnitName"].apply(lambda unit: float(unit_locations[unit][0]))
        grouped_data["longitude"] = grouped_data["UnitName"].apply(lambda unit: float(unit_locations[unit][1]))

        return grouped_data

    heatmap_data = create_unit_heatmap(selected_district, selected_profession, selected_age_district, selected_sex_district, selected_from_year, selected_to_year, selected_from_month, selected_to_month)    
    
    # Display the heatmap and the table of unit names
    district_coordinates = karnataka_districts.get(selected_district, None)
    if district_coordinates and not heatmap_data.empty:
        latitude, longitude = district_coordinates
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": latitude,
                    "longitude": longitude,
                    "zoom": 7,  # Adjust the zoom level as needed
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
                            [0, 0, 255, 255],
                        ],
                    ),
                    district_layer,
                ],
            )
        )
# Assuming you have the necessary variables for the function call

        # Display the table of unit names
        st.subheader("Units in Selected District")
        
        data_frame = table_data(selected_district, selected_age_district, selected_sex_district, selected_from_year, selected_to_year, selected_from_month, selected_to_month)
        # Now use this data_frame to display in the table
        st.table(data_frame[["UnitName", "Male_Count", "Average_Male_Age", "Female_Count", "Average_Female_Age"]])
    else:
        st.warning("No data available for the selected filters or district.")