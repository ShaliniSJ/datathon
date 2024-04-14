import streamlit as st
from PIL import Image
import base64

# Set the page title
st.set_page_config(page_title="Predictive Crime Analysis System")


def set_bg_hack(main_bg):
    
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
            background:url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()}),linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.0));
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            background-blend-mode: overlay;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
set_bg_hack('../images/ksp_logo.png')
# Define the button labels, URLs, and tooltips
button_labels = ["Accused Data Visualisation", "Victim Data Visualisation", "Crime Data Visualisation", "Future Crime Prediction"]
button_urls = ["pages/accusedData.py", "pages/victimData.py", "pages/crimedata.py", "pages/Shalini.py"]  # Replace with actual URLs if needed
button_tooltips = [
    "Explore suspect profiles, associations, and patterns for informed investigations.",
    "Understand victim demographics, vulnerabilities, and impact for victim-centered responses.",
    "Analyze crime hotspots, trends, and modus operandi for proactive policing strategies.",
    "Anticipate emerging crime trends and allocate resources effectively to prevent future incidents."
]

st.title("Predictive Crime Analysis by Enigmatic Energizers")
st.write("")
st.write("")
st.write("")
st.write("")

button_clicked = [False] * 4

# for i in range(4):
#     button_clicked[i] = st.link_button(label=button_labels[i], url=button_urls[i], help=button_tooltips[i],use_container_width = True)

for i in range(len(button_labels)):
    if st.button(label=button_labels[i], help=button_tooltips[i], key=i, use_container_width=True):
        st.switch_page(button_urls[i])