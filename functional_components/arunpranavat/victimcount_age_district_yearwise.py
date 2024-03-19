import streamlit as st
import pandas as pd
import altair as alt

def victim_count_visualization():
    # Load your dataset here
    df = pd.read_csv("D:\\KRK Datathon\\Predictive Crime Analytics\\VictimInfoDetails.csv")

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

# Display the visualization
if __name__ == "__main__":
    victim_count_visualization()
