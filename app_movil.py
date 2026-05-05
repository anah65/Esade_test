import streamlit as st
import pandas as pd
import requests
from streamlit_gps_location import gps_location_button

# ===============================
# 1. Page config
# ===============================
st.set_page_config(page_title="Nearby Restaurants", layout="centered")

st.title("Find Restaurants Near You")

# ===============================
# 2. User input
# ===============================
name = st.text_input("What is your name?")
radius = st.slider("Search radius (meters)", 100, 2000, 1000)

# ===============================
# 3. Get location
# ===============================
st.subheader("Your Location")
location = gps_location_button("Get my location")

# ===============================
# 4. Function to get nearby restaurants
# ===============================
@st.cache_data
def get_nearby_restaurants(lat, lon, radius):
    url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    node
      (around:{radius},{lat},{lon})
      ["amenity"="restaurant"];
    out;
    """

    response = requests.get(url, params={'data': query})
    data = response.json()

    restaurants = []
    for element in data["elements"]:
        name = element.get("tags", {}).get("name", "Unnamed restaurant")
        lat_r = element.get("lat")
        lon_r = element.get("lon")

        restaurants.append({
            "name": name,
            "lat": lat_r,
            "lon": lon_r
        })

    return restaurants


# ===============================
# 5. Main logic
# ===============================
if location is not None and location.get("latitude") is not None:

    lat = location["latitude"]
    lon = location["longitude"]

    st.success(f"Hello {name}! Here are places near you")

    # Map of user
    user_map = pd.DataFrame({"lat": [lat], "lon": [lon]})
    st.map(user_map)

    # Load restaurants
    with st.spinner("Searching for restaurants..."):
        restaurants = get_nearby_restaurants(lat, lon, radius)

    # ===============================
    # 6. Display results
    # ===============================
    st.subheader("🍴 Restaurants nearby")

    if len(restaurants) == 0:
        st.warning("No restaurants found nearby. Try increasing the radius.")
    else:
        # Show list
        for r in restaurants[:10]:
            st.write(f"• {r['name']}")

        # Show on map
        df_map = pd.DataFrame(restaurants)
        st.subheader("Map of nearby restaurants")
        st.map(df_map)

        st.metric(
            "Restaurants found",
            len(restaurants),
            help="Total number of restaurants detected in your area"
        )

else:
    st.info("Click the button to get your location.")
