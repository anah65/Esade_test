import streamlit as st

st.set_page_config(
    page_title="My Mobile App",
    layout="centered"  # IMPORTANT for mobile
)

st.title("📱 My first Streamlit mobile app")

name = st.text_input("What is your name?")
age = st.slider("How old are you?", 0, 100, 25)

if st.button("Submit", use_container_width=True):
    st.success(f"Hello {name}, you are {age} years old 🎉")
