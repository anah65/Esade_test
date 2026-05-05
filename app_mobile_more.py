import streamlit as st
import pandas as pd
from streamlit_gps_location import gps_location_button
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# 1. Page configuration
st.set_page_config(page_title="Bio-Reporter GPS", layout="centered")

# Basic mobile visual style
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Bio-Reporter Pro")
st.write("Record your scientific findings using GPS and photos.")

# 2. User and Report Information
with st.expander("Researcher Information", expanded=True):
    name = st.text_input("Student name:")
    finding_title = st.text_input("What did you find?", placeholder="Example: Anthill, Quartz, Oak...")
    notes = st.text_area("Field notes:", placeholder="Describe the characteristics...")

# 3. GPS Location
st.subheader("1. Location")
location_data = gps_location_button(buttonText="Set GPS Coordinates")

lat, lon = None, None
if location_data:
    lat = location_data.get('latitude')
    lon = location_data.get('longitude')
    if lat and lon:
        st.success(f"Location set: {lat:.5f}, {lon:.5f}")
        # Show small reference map
        df_map = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(df_map, zoom=15)

# 4. Camera
st.subheader("2. Visual Evidence")
photo = st.camera_input("Take a photo of the finding")

# 5. Function to build the PDF
def generate_pdf(name, title, note, photo, lat, lon):
    pdf = FPDF()
    pdf.add_page()
    
    # Decorative header
    pdf.set_fill_color(46, 125, 50)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, 'FIELD REPORT', ln=True, align='C')
    
    # Document body
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, f"Researcher: {name}")
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='R')
    
    # Location data
    pdf.set_font("Arial", 'I', 11)
    if lat and lon:
        pdf.cell(0, 10, f"Coordinates: Lat {lat:.5f}, Lon {lon:.5f}", ln=True)
    
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Title and Description
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Finding: {title}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, f"Observations:\n{note}")
    pdf.ln(10)
    
    # Add image
    if photo:
        img = Image.open(photo)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        img.thumbnail((400, 400))
        
        # Save temporarily for FPDF
        temp_filename = "temp_evidence.jpg"
        img.save(temp_filename, format='JPEG')
        
        pdf.image(temp_filename, x=10, y=None, w=100)
    
    # Avoid encoding issues
    return pdf.output(dest='S').encode('latin-1', errors='replace')

# 6. Final Download Button
if photo and name and finding_title and lat:
    st.divider()
    if st.button("Generate Final Report (PDF)"):
        try:
            pdf_data = generate_pdf(name, finding_title, notes, photo, lat, lon)
            st.download_button(
                label="Download Report",
                data=pdf_data,
                file_name=f"Report_{name.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"There was a problem generating the PDF: {e}")
else:
    st.info("To unlock the PDF: enter your name, a title, capture GPS and take a photo.")
