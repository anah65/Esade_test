import streamlit as st
import pandas as pd
from streamlit_gps_location import gps_location_button
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# 1. Configuración de la página
st.set_page_config(page_title="Bio-Reportero GPS", layout="centered")

# Estilo visual básico para móvil
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

st.title("🌿 Bio-Reportero Pro")
st.write("Registra tus hallazgos científicos con GPS y fotos.")

# 2. Datos del Alumno e Informe
with st.expander("👤 Información del Investigador", expanded=True):
    nombre = st.text_input("Nombre del alumno:")
    titulo_hallazgo = st.text_input("¿Qué has encontrado?", placeholder="Ej: Hormiguero, Cuarzo, Encina...")
    notas = st.text_area("Notas de campo:", placeholder="Describe las características...")

# 3. Ubicación GPS
st.subheader("📍 1. Ubicación")
location_data = gps_location_button(buttonText="Fijar Coordenadas GPS")

lat, lon = None, None
if location_data:
    lat = location_data.get('latitude')
    lon = location_data.get('longitude')
    if lat and lon:
        st.success(f"Ubicación fijada: {lat:.5f}, {lon:.5f}")
        # Mostrar mapa pequeño de referencia
        df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(df_mapa, zoom=15)

# 4. Cámara
st.subheader("📸 2. Evidencia Visual")
foto = st.camera_input("Toma una foto del hallazgo")

# 5. Función para construir el PDF
def generar_pdf(nombre, titulo, nota, foto, lat, lon):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado decorativo
    pdf.set_fill_color(46, 125, 50)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, 'INFORME DE CAMPO', ln=True, align='C')
    
    # Cuerpo del documento
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, f"Investigador: {nombre}")
    pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='R')
    
    # Datos de ubicación
    pdf.set_font("Arial", 'I', 11)
    if lat and lon:
        pdf.cell(0, 10, f"Coordenadas: Lat {lat:.5f}, Lon {lon:.5f}", ln=True)
    
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Título y Descripción
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Hallazgo: {titulo}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, f"Observaciones:\n{nota}")
    pdf.ln(10)
    
    # Añadir la foto
    if foto:
        img = Image.open(foto)
        # Redimensionar para que quepa en el PDF manteniendo proporción
        img.thumbnail((400, 400))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        pdf.image(img_buffer, x=10, y=None, w=100)
    
    return pdf.output(dest='S').encode('latin-1')

# 6. Botón Final de Descarga
if foto and nombre and titulo_hallazgo and lat:
    st.divider()
    if st.button("🛠️ Generar Informe Final (PDF)"):
        try:
            pdf_data = generar_pdf(nombre, titulo_hallazgo, notas, foto, lat, lon)
            st.download_button(
                label="📥 DESCARGAR INFORME",
                data=pdf_data,
                file_name=f"Informe_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Hubo un problema al crear el PDF: {e}")
else:
    st.info("💡 Para desbloquear el PDF: Escribe tu nombre, un título, captura el GPS y haz una foto.")