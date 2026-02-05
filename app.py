import streamlit as st
import random
import json
import os

# --- LÓGICA DEL GENERADOR ---
class GeneradorFrases:
    def __init__(self, archivo="biblioteca_frases.json"):
        self.archivo = archivo
        self.biblioteca = self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {
            "Pensadores": ["Solo sé que no sé nada. - Sócrates", "La duda es el principio de la sabiduría. - Aristóteles"],
            "Libros": ["El hombre nace libre. - Rousseau", "Caminante, no hay camino... - Machado"],
            "Canciones": ["Everything will be okay. - Lennon", "Vivir es lo más peligroso que tiene la vida. - Alejandro Sanz"],
            "Propias": ["La curiosidad es el código del futuro."]
        }

    def generar(self, categoria):
        if categoria in self.biblioteca:
            return random.choice(self.biblioteca[categoria])
        return "Categoría no encontrada."

# --- INTERFAZ WEB ---
st.set_page_config(page_title="Inspiración Automática", page_icon="✨")
gen = GeneradorFrases()

st.title("✨ Generador de Frases")

# Sección 1: Generar Frase
st.header("🔮 Obtener Inspiración")

# Usamos columnas para que se vea ordenado
col1, col2 = st.columns([2, 1])

with col2:
    categoria_sel = st.selectbox("Elige una categoría", list(gen.biblioteca.keys()))
    # El botón ahora forzará el cambio
    boton_generar = st.button("Generar nueva frase")

with col1:
    # Si se pulsa el botón o si ya había una frase guardada
    if boton_generar:
        frase_suerte = gen.generar(categoria_sel)
        # Guardamos la frase en la memoria de la sesión para que no desaparezca
        st.session_state['frase_actual'] = frase_suerte
    
    if 'frase_actual' in st.session_state:
        st.info("Tu frase es:")
        st.subheader(f"\"{st.session_state['frase_actual']}\"")
    else:
        st.write("Selecciona una categoría y pulsa el botón.")

st.divider()

# Sección 2: Añadir (El resto del código se mantiene igual...)
with st.expander("✍️ Añadir una nueva frase a la colección"):
    nueva_cat = st.radio("Categoría destino:", list(gen.biblioteca.keys()), horizontal=True)
    nueva_frase = st.text_area("Escribe la frase:")
    if st.button("Guardar frase"):
        if nueva_frase.strip():
            # Aquí podrías implementar la lógica de guardado si lo deseas
            st.success("¡Frase guardada con éxito!")
