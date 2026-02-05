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
            "Pensadores": ["Solo sé que no sé nada. - Sócrates"],
            "Libros": ["El hombre nace libre. - Rousseau"],
            "Canciones": ["Everything will be okay. - Lennon"],
            "Propias": ["La curiosidad es el código del futuro."]
        }

    def guardar_datos(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.biblioteca, f, indent=4, ensure_ascii=False)

    def añadir_frase(self, categoria, frase):
        if categoria in self.biblioteca:
            self.biblioteca[categoria].append(frase)
            self.guardar_datos()

    # ESTA ES LA FUNCIÓN QUE FALTABA O DABA ERROR
    def generar(self, categoria=None):
        if not categoria or categoria not in self.biblioteca:
            categoria = random.choice(list(self.biblioteca.keys()))
        return random.choice(self.biblioteca[categoria])

# --- INTERFAZ WEB CON STREAMLIT ---
st.set_page_config(page_title="Inspiración Automática", page_icon="✨")
gen = GeneradorFrases()

st.title("✨ Generador de Frases")
st.markdown("Obtén inspiración de pensadores, libros, música o de ti mismo.")

# Sección 1: Generar Frase
st.header("🔮 Obtener Inspiración")
col1, col2 = st.columns([2, 1])

with col2:
    categoria_sel = st.selectbox("Elige una categoría", list(gen.biblioteca.keys()))
    boton_generar = st.button("Generar Frase")

with col1:
    if boton_generar:
        frase_suerte = gen.generar(categoria_sel) # Ahora sí funcionará
        st.subheader(f"\"{frase_suerte}\"")
    else:
        st.info("Haz clic en el botón para mostrar una frase.")

st.divider()

# Sección 2: Añadir Contenido
st.header("✍️ Añadir a la Colección")
with st.expander("Haz clic aquí para guardar una frase nueva"):
    nueva_cat = st.radio("Categoría:", list(gen.biblioteca.keys()), horizontal=True)
    nueva_frase = st.text_area("Escribe la frase y su autor:")
    
    if st.button("Guardar permanentemente"):
        if nueva_frase.strip():
            gen.añadir_frase(nueva_cat, nueva_frase)
            st.success(f"¡Frase guardada en {nueva_cat}! (Nota: Se verá reflejada en esta sesión).")
        else:
            st.warning("Escribe algo antes de guardar.")
