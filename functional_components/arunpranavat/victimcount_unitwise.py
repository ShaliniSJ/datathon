import streamlit as st
import pandas as pd
import altair as alt

def victim_count_visualization():
    st.title("Comparing Victim Count Unit wise")

    # Load your dataset here
    df = pd.read_csv("D:\\KRK Datathon\\Predictive Crime Analytics\\VictimInfoDetails.csv")

    # Filter the data to include only relevant columns
    df_filtered = df[['District_Name', 'UnitName', 'Year', 'Victim_ID']]

    # Create a multi-select widget for choosing districts
    selected_district = st.selectbox("Choose District", list(df_filtered['District_Name'].unique()))

    # Filter the data based on selected district
    filtered_data = df_filtered[df_filtered['District_Name'] == selected_district]

    # Group by unit name and year and count occurrences
    unit_counts = filtered_data.groupby(['UnitName', 'Year']).size().reset_index(name='Victim Count')

    # Create a chart to visualize victim counts per unit
    chart = alt.Chart(unit_counts).mark_bar().encode(
        x='Year:N',
        y='Victim Count:Q',
        color='UnitName:N'
    ).properties(
        width=600,
        height=300,
        title=f"Victim Count Unit wise for {selected_district}"
    )

    st.write(chart)

# Display the visualization
if __name__ == "__main__":
    victim_count_visualization()
