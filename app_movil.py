import streamlit as st
from streamlit_gps_location import gps_location_button

st.set_page_config(
    page_title="My Mobile App",
    layout="centered"  # IMPORTANT for mobile
)

st.title("📱 My first Streamlit mobile app")

name = st.text_input("What is your name?")
age = st.slider("How old are you?", 0, 100, 25)

# Button to get GPS location
st.subheader("📍 Location")
location_data = gps_location_button(buttonText="Get my location")

if location_data:
    st.write("Your location data:")
    st.json(location_data)

if st.button("Submit", use_container_width=True):
    st.success(f"Hello {name}, you are {age} years old 🎉")
