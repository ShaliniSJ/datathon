import streamlit as st
import pandas as pd
import altair as alt

def victim_count_visualization():
    st.title("Victim Data Visualization")

    # Load your dataset here
    df = pd.read_csv("D:\\KRK Datathon\\Predictive Crime Analytics\\VictimInfoDetails.csv")

    # Create a dropdown list for selecting the type of comparison
    comparison_type = st.selectbox(
        "Choose comparison type",
        ["Victim Count per Age Range", "Unit-wise Victim Count", "Injury Type Comparison"]
    )

    if comparison_type == "Victim Count per Age Range":
        st.subheader("Victim Count per Age Range")

        # Calculate victim count per age range, district, and year
        victim_counts = df.groupby(['District_Name', 'Year', pd.cut(df['age'], bins=[0, 18, 30, 45, 60, 100], labels=['0-18', '19-30', '31-45', '46-60', '61+'])]).size().reset_index(name='Victim Count')

        # Create a multi-select widget for choosing districts
        selected_districts = st.multiselect("Choose Districts", list(victim_counts['District_Name'].unique()))

        # Filter the data based on selected districts
        filtered_data = victim_counts[victim_counts['District_Name'].isin(selected_districts)]

        # Create a chart to visualize victim counts
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x='Year:N',
            y='Victim Count:Q',
            color='age:N',
            column='District_Name:N'
        ).properties(
            width=600,
            height=300
        )

        st.write(chart)

    elif comparison_type == "Unit-wise Victim Count":
        st.subheader("Unit-wise Victim Count")

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

    elif comparison_type == "Injury Type Comparison":
        st.subheader("Injury Type Comparison")

        # Filter the data to include only relevant columns
        df_filtered = df[['District_Name', 'Year', 'InjuryType']]

        # Group by district, year, and injury type and count occurrences
        grouped_data = df_filtered.groupby(['District_Name', 'Year', 'InjuryType']).size().reset_index(name='Count')

        # Create a multi-select widget for choosing districts
        selected_districts = st.multiselect("Choose Districts", list(grouped_data['District_Name'].unique()))

        # Filter the data based on selected districts
        filtered_data = grouped_data[grouped_data['District_Name'].isin(selected_districts)]

        # Create a chart to visualize injury types
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

# Display the visualization based on the selected comparison type
if __name__ == "__main__":
    victim_count_visualization()
