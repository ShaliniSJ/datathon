import streamlit as st
import pandas as pd
import pydeck as pdk

# Load victim data from Parquet file
mapped_data = pd.read_parquet("D:\\KRK Datathon\\Predictive Crime Analytics\\VictimInfoDetails.parquet")

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

# Filter relevant columns
victim_data = mapped_data[["District_Name", "Year", "age", "InjuryType", "UnitName", "Profession"]]

# Group data for graphs
district_year_age = victim_data.groupby(["District_Name", "Year", "age"]).size().reset_index(name="VictimCount")
district_injury_year = victim_data.groupby(["District_Name", "InjuryType", "Year"]).size().reset_index(name="VictimCount")
district_unit_count = victim_data.groupby(["District_Name", "UnitName"]).size().reset_index(name="VictimCount")
district_profession_count = victim_data.groupby(["District_Name", "Profession"]).size().reset_index(name="VictimCount")

# Add latitude and longitude columns to each DataFrame using the karnataka_districts dictionary
district_year_age["latitude"] = district_year_age["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[0])
district_year_age["longitude"] = district_year_age["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[1])

district_injury_year["latitude"] = district_injury_year["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[0])
district_injury_year["longitude"] = district_injury_year["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[1])

district_unit_count["latitude"] = district_unit_count["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[0])
district_unit_count["longitude"] = district_unit_count["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[1])

district_profession_count["latitude"] = district_profession_count["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[0])
district_profession_count["longitude"] = district_profession_count["District_Name"].map(lambda x: karnataka_districts.get(x, (None, None))[1])



def mapping_demo(data, layers):
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": 14.5204, "longitude": 75.7224, "zoom": 7, "pitch": 50},
            layers=layers,
        )
    )

# Define pydeck layers for different graphs
ALL_LAYERS = {
    "Victim Count District-wise based on Year and Age": pdk.Layer(
        "ScatterplotLayer",
        data=district_year_age,
        get_position=["longitude", "latitude"],
        get_color="[VictimCount, 0, 255, 255]",
        get_radius=1000,
    ),
    "Victim Count District-wise based on Injury Type and Year": pdk.Layer(
        "ScatterplotLayer",
        data=district_injury_year,
        get_position=["longitude", "latitude"],
        get_color="[VictimCount, 255, 0, 255]",
        get_radius=1000,
    ),
    "Victim Count Unit-wise in Each District": pdk.Layer(
        "ScatterplotLayer",
        data=district_unit_count,
        get_position=["longitude", "latitude"],
        get_color="[VictimCount, 255, 255, 0]",
        get_radius=1000,
    ),
    "Victim Count Profession-wise in Each District": pdk.Layer(
        "ScatterplotLayer",
        data=district_profession_count,
        get_position=["longitude", "latitude"],
        get_color="[VictimCount, 255, 0, 0]",
        get_radius=1000,
    ),
}

st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")

mapping_demo(karnataka_districts, ALL_LAYERS)
