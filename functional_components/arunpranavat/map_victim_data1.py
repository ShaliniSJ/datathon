import streamlit as st
import pandas as pd
import pydeck as pdk

# Load victim data
mapped_data = pd.read_csv("D:\\KRK Datathon\\Predictive Crime Analytics\\VictimInfoDetails.csv")

# Coordinates of Karnataka districts
karnataka_districts = {
    "Bagalkot": (16.2000, 75.7700),
    "Bangalore Rural": (12.9716, 77.5762),
    "Bangalore Urban": (12.9716, 77.5762),
    "Belagavi": (15.8644, 74.5006),
    "Bellary": (15.1500, 76.6000),
    "Bidar": (17.9228, 77.5167),
    "Bijapur": (16.8200, 75.7700),
    "Chamarajanagara": (11.9300, 76.5700),
    "Chikmagalur": (13.3300, 75.7700),
    "Chitradurga": (14.1500, 76.4000),
    "Dakshina Kannada": (12.9716, 77.5762),
    "Davangere": (14.4800, 75.9200),
    "Dharwad": (15.4700, 75.0000),
    "Gadag": (15.4200, 75.8200),
    "Gulbarga": (17.9000, 76.8000),
    "Hassan": (12.7800, 76.1000),
    "Haveri": (14.4800, 75.5200),
    "Kodagu": (11.6300, 75.7700),
    "Kolar": (12.1300, 78.1300),
    "Koppal": (15.3000, 76.1700),
    "Mandya": (12.5200, 76.9000),
    "Raichur": (16.0200, 76.3800),
    "Ramanagara": (12.7300, 77.6300),
    "Shimoga": (14.6300, 75.5700),
    "Tumkur": (13.3500, 77.1000),
    "Udupi": (13.3300, 74.7800),
    "Uttara Kannada": (14.7800, 74.1000),
    "Yadgir": (16.8000, 77.0200)
}

# Function to get coordinates (latitude, longitude) for a given district
def get_coordinates(district):
    return karnataka_districts.get(district, (None, None))

# Add latitude and longitude columns to mapped_data using get_coordinates function
mapped_data['Latitude'] = mapped_data['District_Name'].apply(lambda x: get_coordinates(x)[0])
mapped_data['Longitude'] = mapped_data['District_Name'].apply(lambda x: get_coordinates(x)[1])

# Filter out rows with missing coordinates
mapped_data = mapped_data.dropna(subset=['Latitude', 'Longitude'])

# Set initial view state for the map
view_state = pdk.ViewState(
    latitude=15.3173,
    longitude=75.7139,
    zoom=7,
    pitch=50,
)

# Create pydeck map layers
layer = pdk.Layer(
    "ScatterplotLayer",
    data=mapped_data,
    get_position=["Longitude", "Latitude"],
    get_radius=50,  # Adjust radius for better visualization
    get_color="[200, 30, 0, 160]",
    pickable=True,
)

# Create pydeck map
map_ = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[layer],
)

# Display the map
if __name__ == '__main__':
    st.pydeck_chart(map_)

# Plot graphs based on age and injury type directly on the map
st.subheader("Victim Data Analysis")
st.write("### Age-wise Analysis")
age_count = mapped_data['age'].value_counts().reset_index()
age_count.columns = ['age', 'count']
st.pydeck_chart(pdk.Deck(
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=age_count,
            get_position=["Longitude", "Latitude"],
            get_radius="count",
            get_color="[200, 30, 0, 160]",
            pickable=True,
        )
    ],
    initial_view_state=view_state,
))

st.write("### Injury Type Analysis")
injury_count = mapped_data['InjuryType'].value_counts().reset_index()
injury_count.columns = ['InjuryType', 'count']
st.pydeck_chart(pdk.Deck(
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=injury_count,
            get_position=["Longitude", "Latitude"],
            get_radius="count",
            get_color="[200, 30, 0, 160]",
            pickable=True,
        )
    ],
    initial_view_state=view_state,
))
