# import streamlit as st
# import pandas as pd
# import pydeck as pdk
# import json

# # Function to load accused data
# @st.cache(allow_output_mutation=True)
# def get_accused_data(filename):
#     df = pd.read_csv(filename)
#     # Categorize the age data into specified groups
#     bins = [0, 18, 25, 45, 60, float('inf')]
#     labels = ['0-18', '19-25', '26-45', '46-60', '61+']
#     df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
#     return df

# # Function to load GeoJSON data
# @st.cache(allow_output_mutation=True)
# def load_geojson(filename):
#     with open(filename) as f:
#         return json.load(f)

# # Function to create age distribution layer
# def create_age_distribution_layer(data, geojson_features):
#     # Create DataFrame from GeoJSON features
#     features_df = pd.json_normalize(geojson_features, 'features')
#     # Get a DataFrame with district names and corresponding coordinates
#     district_coords = features_df[['properties.district', 'geometry.coordinates']]
#     district_coords = district_coords.explode('geometry.coordinates').reset_index(drop=True)
    
#     # Prepare the data for PyDeck
#     layer_data = pd.merge(district_coords, data, how='left', left_on='properties.district', right_on='District_Name')
#     layer_data = layer_data[['geometry.coordinates', 'age_group', 'count']].dropna()
#     layer_data['position'] = layer_data['geometry.coordinates'].apply(lambda coords: coords[0][0])

#     return pdk.Layer(
#         "ColumnLayer",
#         data=layer_data,
#         disk_resolution=12,
#         radius=250,
#         extruded=True,
#         pickable=True,
#         elevation_scale=30,
#         getPosition='position',
#         getFillColor=[255, 165, 0, 80],
#         getElevation='count'
#     )

# # Main block
# try:
#     # Load data
#     csv_path = 'C:\\Users\\Legion\\Desktop\\KSP DATATHON\\datathon\\functional_components\\Predictive Crime Analytics\\AccusedData.csv'
#     geojson_path = 'C:\\Users\\Legion\\Desktop\\KSP DATATHON\\datathon\\functional_components\\images\\karnataka.json'
#     accused_data = get_accused_data(csv_path)
#     geojson_data = load_geojson(geojson_path)

#     # UI for selecting the district
#     district_options = accused_data['District_Name'].unique()
#     selected_district = st.selectbox('Select a district:', district_options)

#     # Convert GeoJSON properties to DataFrame for styling and merge with district names
#     geojson_properties_df = pd.json_normalize(geojson_data['features'], 'properties')
#     geojson_properties_df['style'] = geojson_properties_df['district'].apply(
#         lambda x: {'fillOpacity': 0.4, 'fillColor': '#0078ff'} if x == selected_district else {'fillOpacity': 0.1, 'fillColor': '#aaaaaa'}
#     )
#     # Merge the styling information back into the GeoJSON dictionary
#     for feature, style in zip(geojson_data['features'], geojson_properties_df['style']):
#         feature['properties']['style'] = style
    
#     # PyDeck layer for GeoJSON
#     geojson_layer = pdk.Layer(
#         'GeoJsonLayer',
#         geojson_data,
#         opacity=0.8,
#         stroked=False,
#         filled=True,
#         extruded=True,
#         wireframe=True,
#         get_elevation='properties.style.fillOpacity',
#         get_fill_color='properties.style.fillColor',
#         get_line_color=[255, 255, 255],
#     )

#     # Set the initial view state
#     initial_view_state = pdk.ViewState(
#         latitude=12.9716,
#         longitude=77.5946,
#         zoom=6,
#         pitch=50
#     )
#     # Render the map with the layers
#     st.pydeck_chart(pdk.Deck(
#         map_style='mapbox://styles/mapbox/light-v9',
#         initial_view_state=initial_view_state,
#         layers=[geojson_layer] + ([create_age_distribution_layer(accused_data[accused_data['District_Name'] == selected_district], geojson_data['features'])] if selected_district else []),
#     ))

# except Exception as e:
#     st.error(f"An error occurred: {e}")
import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import math

# Load the GeoJSON file for Karnataka districts
geojson_path = 'C:\\Users\\Legion\\Desktop\\KSP DATATHON\\datathon\\functional_components\\images\\karnataka.json'
with open(geojson_path, 'r') as f:
    geojson_data = json.load(f)

# Initialize the session state for the currently selected district and zoom level
if 'selected_district' not in st.session_state:
    st.session_state.selected_district = None
if 'zoom_level' not in st.session_state:
    st.session_state.zoom_level = 6
if 'initial_location' not in st.session_state:
    st.session_state.initial_location = [12.9716, 77.5946]

# Function to calculate zoom level based on map bounds and window size
def calculate_zoom_level(min_lon, min_lat, max_lon, max_lat):
    WORLD_DIM = {'height': 256, 'width': 256}
    ZOOM_MAX = 21

    lat_rad = math.radians(max_lat)
    n = 2.0 ** ZOOM_MAX
    zoom_lat_rad = math.log(n * (1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad))) / 2.0
    zoom_lat_deg = math.degrees(zoom_lat_rad)

    lat_fraction = (zoom_lat_deg + max_lat) / max_lat
    lng_delta_deg = max_lon - min_lon
    lng_delta_zoomed = lng_delta_deg * lat_fraction

    return int(ZOOM_MAX - math.log(WORLD_DIM['width'] / lng_delta_zoomed) / math.log(2))

# Create a base map with the initial location
m = folium.Map(location=st.session_state.initial_location, zoom_start=st.session_state.zoom_level)

# Define a function to change the color of the districts based on selection
def style_function(feature):
    district_name = feature['properties']['district']  # Make sure this matches your GeoJSON property
    if district_name == st.session_state.selected_district:
        return {'fillColor': 'green', 'color': 'black', 'weight': 1, 'fillOpacity': 0.6}
    else:
        return {'fillColor': 'blue', 'color': 'black', 'weight': 1, 'fillOpacity': 0.6}

# Create a GeoJson layer
geojson_layer = folium.GeoJson(
    geojson_data,
    name='Karnataka',
    style_function=style_function
)
geojson_layer.add_to(m)

# Display the map
folium_static(m)

# Simulate district selection
district_options = [feature['properties']['district'] for feature in geojson_data['features']]  # Use the correct key here
selected_district = st.selectbox('Select a district:', district_options)

# Check if the selected district has changed
if st.session_state.selected_district != selected_district:
    # Update the selected district
    st.session_state.selected_district = selected_district
    # Zoom to the selected district
    district_geometry = next((feature['geometry'] for feature in geojson_data['features'] if feature['properties']['district'] == selected_district), None)
    if district_geometry:
        bounds = folium.GeoJson(district_geometry).get_bounds()
        zoom_level = calculate_zoom_level(bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])
        st.session_state.zoom_level = zoom_level
        m.fit_bounds(bounds, padding=(20, 20))  # Adjust padding
    # Update the style of the existing GeoJson layer
    geojson_layer.style_function = style_function
    folium_static(m)

# Add a "Clear" button to clear all district highlights and reset the map to its original state
if st.button('Clear'):
    st.session_state.selected_district = None
    st.session_state.zoom_level = 6
    m.location = st.session_state.initial_location  # Reset to initial location
    m.zoom_start = st.session_state.zoom_level
    geojson_layer.style_function = style_function  # Update the style to clear the highlights
    folium_static(m)
