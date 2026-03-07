import streamlit as st
from groq import Groq

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Inspiración Infinita IA", page_icon="🎨")

# Conectar con la llave secreta
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Configura la GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Estilos de colores
estilos = {
    "Filósofos": {"color": "#1E3A8A", "bg": "#DBEAFE", "icon": "🏛️"},
    "Libros": {"color": "#065F46", "bg": "#D1FAE5", "icon": "📖"},
    "Canciones": {"color": "#991B1B", "bg": "#FEE2E2", "icon": "🎸"},
    "Propias": {"color": "#92400E", "bg": "#FEF3C7", "icon": "💡"},
    "Destino (Azar)": {"color": "#5B21B6", "bg": "#EDE9FE", "icon": "🎲"}
}

def generar_frase_ia(categoria):
    # Prompt optimizado para evitar errores 400
    mensaje_prompt = f"Genera una frase corta y profunda de la categoría {categoria}. Solo responde con la frase y el autor."
    
    try:
        # Usamos el modelo 'llama-3.3-70b-versatile' que es el más actualizado y estable
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un generador de frases sabias y creativas."},
                {"role": "user", "content": mensaje_prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Si falla el modelo anterior, intentamos con el modelo pequeño
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": mensaje_prompt}]
            )
            return completion.choices[0].message.content
        except:
            return f"Hubo un pequeño error técnico. Intenta de nuevo. (Detalle: {str(e)[:30]})"

# --- INTERFAZ ---
st.title("🚀 Sabiduría Infinita con IA")

if 'frase_actual' not in st.session_state:
    st.session_state.frase_actual = "Haz clic para generar tu primera frase única."
if 'cat_actual' not in st.session_state:
    st.session_state.cat_actual = "Destino (Azar)"

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Opciones")
    categoria = st.selectbox("Elige el estilo:", list(estilos.keys()))
    if st.button("✨ GENERAR FRASE"):
        with st.spinner('Consultando a la IA...'):
            st.session_state.frase_actual = generar_frase_ia(categoria)
            st.session_state.cat_actual = categoria
        st.rerun()

# Mostrar la frase con su color correspondiente
estilo = estilos[st.session_state.cat_actual]
st.markdown(f"""
    <div style="
        padding: 30px; 
        border-radius: 20px; 
        background-color: {estilo['bg']}; 
        border-left: 10px solid {estilo['color']};
        color: {estilo['color']};
        font-size: 24px;
        font-family: 'serif';
    ">
        {estilo['icon']} <i>{st.session_state.frase_actual}</i>
    </div>
    """, unsafe_allow_html=True)
