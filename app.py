import streamlit as st
import random
from groq import Groq

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Inspiración Infinita IA", page_icon="🎨")

# Cliente de IA (Usando el Secret de Streamlit)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")

# Diccionario de Colores y Estilos
estilos = {
    "Filósofos": {"color": "#1E3A8A", "bg": "#DBEAFE", "icon": "🏛️"}, # Azul
    "Libros": {"color": "#065F46", "bg": "#D1FAE5", "icon": "📖"},    # Verde
    "Canciones": {"color": "#991B1B", "bg": "#FEE2E2", "icon": "🎸"}, # Rojo
    "Propias": {"color": "#92400E", "bg": "#FEF3C7", "icon": "💡"},   # Ámbar
    "Destino (Azar)": {"color": "#5B21B6", "bg": "#EDE9FE", "icon": "🎲"} # Púrpura
}

def generar_frase_ia(categoria):
    prompt = f"Genera una frase única, profunda y original de la categoría: {categoria}. Que no sea famosa, inventa algo nuevo con ese estilo. Solo devuelve la frase y el autor ficticio."
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8, # Más creatividad
        )
        return completion.choices[0].message.content
    except:
        return "El universo está en silencio ahora mismo. (Error de conexión)"

# --- INTERFAZ ---
st.title("🚀 Generador de Sabiduría Infinita")

if 'frase_actual' not in st.session_state:
    st.session_state.frase_actual = "Haz clic para despertar a la IA..."
if 'cat_actual' not in st.session_state:
    st.session_state.cat_actual = "Destino (Azar)"

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Configuración")
    categoria = st.selectbox("Elige la fuente:", list(estilos.keys()))
    if st.button("✨ GENERAR NUEVA FRASE"):
        with st.spinner('La IA está pensando...'):
            st.session_state.frase_actual = generar_frase_ia(categoria)
            st.session_state.cat_actual = categoria

# Aplicar Colores Dinámicos
estilo = estilos[st.session_state.cat_actual]
st.markdown(f"""
    <div style="
        padding: 30px; 
        border-radius: 20px; 
        background-color: {estilo['bg']}; 
        border-left: 10px solid {estilo['color']};
        color: {estilo['color']};
        font-family: 'Georgia', serif;
        font-size: 24px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    ">
        {estilo['icon']} <i>"{st.session_state.frase_actual}"</i>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.info("Cada frase es generada por una red neuronal en tiempo real. Nunca verás la misma dos veces.")
