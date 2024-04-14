import streamlit as st

# Function to get unit names based on selected district
def get_unit_names(district):
    # Dummy data, replace this with actual data source
    units = {
        "balagot": ["amengad ps", "unit2", "unit3"],
        "ballari": ["unit1", "unit2", "unit3"],
        # Add more districts and unit names as needed
    }
    return units.get(district, [])

def main():
    st.title("Future Crime Prediction")

    # Get inputs from user

    type_input = st.selectbox("Select Type", ["State", "District", "Unit"])

    if type_input == "State":
        # Only one option for Karnataka
        state = "Karnataka"
        st.write(f"Selected State: {state}")

    elif type_input == "District":
        # All districts and select district
        districts = ["All", "Balagot", "Ballari", "Other 31 Districts"]
        selected_district = st.selectbox("Select District", districts)

        if selected_district != "All":
            st.write(f"Selected District: {selected_district}")

    else:  # Unit
        selected_district = st.selectbox("Select District", ["Balagot", "Ballari", "Other 31 Districts"])
        unit_names = get_unit_names(selected_district)
        selected_unit = st.selectbox("Select Unit", unit_names)

        st.write(f"Selected Unit: {selected_unit}")

    date_range = st.date_input("Select Date Range")

    crime_types = ["All", "Theft", "Kidnap", "Other 107 types of crime"]
    selected_crime_type = st.selectbox("Select Type of Crime", crime_types)

    st.write("Date Range:", date_range)
    st.write("Type of Crime:", selected_crime_type)


if __name__ == "__main__":
    main()
