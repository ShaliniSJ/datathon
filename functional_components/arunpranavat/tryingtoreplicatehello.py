import streamlit as st
import pandas as pd
import pydeck as pdk

# Load victim data from Parquet file
mapped_data = pd.read_csv(r"D:\KRK Datathon\Predictive Crime Analytics\VictimInfoDetails.csv")

# Coordinates of Karnataka districts
karnataka_districts = {
    "Bagalkot": (16.1852, 75.6966),
    "Ballari": (15.1394, 76.9214),
    "Belagavi City": (15.8497, 74.4977),
    "Belagavi Dist": (15.8497, 74.4977),
    "Bengaluru City": (12.9716, 77.5946),
    "Bengaluru Dist": (12.9716, 77.5946),
    "Bidar": (17.9137, 77.5175),
    "Chamarajanagar": (11.9261, 76.9432),
    "Chickballapura": (13.4352, 77.7338),
    "Chikkamagaluru": (13.3153, 75.7754),
    "Chitradurga": (14.23, 76.3985),
    "CID": (12.9716, 77.5946),
    "Coastal Security Police": (12.9716, 77.5946),
    "Dakshina Kannada": (12.8654, 74.8426),
    "Davanagere": (14.4664, 75.9238),
    "Dharwad": (15.3647, 75.1239),
    "Gadag": (15.4296, 75.6299),
    "Hassan": (13.0072, 76.096),
    "Haveri": (14.7959, 75.3952),
    "Hubballi Dharwad City": (15.3647, 75.1239),
    "ISD Bengaluru": (12.9716, 77.5946),
    "K.G.F": (12.9716, 77.5946),
    "Kalaburagi": (17.3297, 76.8343),
    "Kalaburagi City": (17.3297, 76.8343),
    "Karnataka Railways": (12.9716, 77.5946),
    "Kodagu": (12.3375, 75.8069),
    "Kolar": (13.1364, 78.1299),
    "Koppal": (15.3506, 76.1546),
    "Mandya": (12.5223, 76.8974),
    "Mangaluru City": (12.9141, 74.856),
    "Mysuru City": (12.2958, 76.6394),
    "Mysuru Dist": (12.2958, 76.6394),
    "Raichur": (16.2, 77.355),
    "Ramanagara": (12.7159, 77.2813),
    "Shivamogga": (13.9299, 75.5681),
    "Tumakuru": (13.3422, 77.1016),
    "Udupi": (13.3409, 74.7421),
    "Uttara Kannada": (14.9656, 74.4101),
    "Vijayanagara": (15.335, 76.4626),
    "Vijayapur": (16.8302, 75.7109),
    "Yadgir": (16.7704, 77.1305)
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



def mapping_demo(layers):
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
        get_radius=10000,
    ),
    "Victim Count District-wise based on Injury Type and Year": pdk.Layer(
        "ScatterplotLayer",
        data=district_injury_year,
        get_position=["longitude", "latitude"],
        get_color="[VictimCount, 255, 0, 255]",
        get_radius=10000,
    ),
    "Victim Count Unit-wise in Each District": pdk.Layer(
        "ScatterplotLayer",
        data=district_unit_count,
        get_position=["longitude", "latitude"],
        get_color="[VictimCount, 255, 255, 0]",
        get_radius=10000,
    ),
    "Victim Count Profession-wise in Each District": pdk.Layer(
        "ScatterplotLayer",
        data=district_profession_count,
        get_position=["longitude", "latitude"],
        get_color="[VictimCount, 255, 0, 0]",
        get_radius=10000,
    ),
}

# Define the main function
def main():
    st.set_page_config(page_title="KSP Crime Analytics", page_icon="🌍")
    st.markdown("# Mapping Demo")
    st.sidebar.header("Mapping Demo")
    
    selected_layer = st.sidebar.radio("Select Layer", list(ALL_LAYERS.keys()))
    
    # Show selected layer
    mapping_demo([ALL_LAYERS[selected_layer]])

if __name__ == "__main__":
    main()