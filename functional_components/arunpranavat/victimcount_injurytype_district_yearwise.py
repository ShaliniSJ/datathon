import streamlit as st
import pandas as pd
import altair as alt

def injury_type_visualization():
    st.title("Comparing Injury type of Victims District wise and Year wise")

    # Load your dataset here
    df = pd.read_csv("D:\\KRK Datathon\\Predictive Crime Analytics\\VictimInfoDetails.csv")

    # Filter the data to include only relevant columns
    df_filtered = df[['District_Name', 'Year', 'InjuryType']]

    # Group by district, year, and injury type and count occurrences
    grouped_data = df_filtered.groupby(['District_Name', 'Year', 'InjuryType']).size().reset_index(name='Count')

    # Create a multi-select widget for choosing districts
    selected_districts = st.multiselect("Choose Districts", list(grouped_data['District_Name'].unique()))

    # Filter the data based on selected districts
    filtered_data = grouped_data[grouped_data['District_Name'].isin(selected_districts)]

    # Create a chart to visualize injury types per district
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x='Year:N',
        y='Count:Q',
        color='InjuryType:N',
        column='District_Name:N'
    ).properties(
        width=600,
        height=300
    )

    st.write(chart)

    # Calculate total victim count based on injury type for Karnataka
    total_victims_karnataka = df[df['District_Name'].str.contains("Karnataka")].groupby(['Year', 'InjuryType']).size().reset_index(name='Total Count')

    # Create a chart to visualize total victim count for Karnataka
    total_chart = alt.Chart(total_victims_karnataka).mark_bar().encode(
        x='Year:N',
        y='Total Count:Q',
        color='InjuryType:N',
    ).properties(
        width=600,
        height=300,
        title='Total Victim Count for Karnataka (All Districts Combined)'
    )

    st.write(total_chart)

if __name__ == "__main__":
    # Display the visualization
    injury_type_visualization()
