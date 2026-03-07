import streamlit as st
import random
from groq import Groq

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Inspiración Infinita IA", page_icon="🎨")

# 1. INTENTAR CONECTAR CON LA LLAVE
try:
    # Buscamos la llave en los Secrets de Streamlit
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
    else:
        st.error("❌ No se encontró la llave 'GROQ_API_KEY' en los Secrets.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Error de configuración: {e}")
    st.stop()

# Diccionario de Colores
estilos = {
    "Filósofos": {"color": "#1E3A8A", "bg": "#DBEAFE", "icon": "🏛️"},
    "Libros": {"color": "#065F46", "bg": "#D1FAE5", "icon": "📖"},
    "Canciones": {"color": "#991B1B", "bg": "#FEE2E2", "icon": "🎸"},
    "Propias": {"color": "#92400E", "bg": "#FEF3C7", "icon": "💡"},
    "Destino (Azar)": {"color": "#5B21B6", "bg": "#EDE9FE", "icon": "🎲"}
}

def generar_frase_ia(categoria):
    prompt = f"Genera una frase corta, profunda y original de la categoría: {categoria}. Solo la frase y el autor."
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"La IA está descansando. Error: {str(e)[:50]}..."

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
        with st.spinner('Pensando...'):
            st.session_state.frase_actual = generar_frase_ia(categoria)
            st.session_state.cat_actual = categoria

# Cuadro con Color Dinámico
estilo = estilos[st.session_state.cat_actual]
st.markdown(f"""
    <div style="padding: 30px; border-radius: 20px; background-color: {estilo['bg']}; 
    border-left: 10px solid {estilo['color']}; color: {estilo['color']}; font-size: 24px;">
        {estilo['icon']} <i>"{st.session_state.frase_actual}"</i>
    </div>
    """, unsafe_allow_html=True)
