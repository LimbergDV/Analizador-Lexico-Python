import pandas as pd
import re
import streamlit as st

# ------------------------------
# REGEX
# ------------------------------
ER_PALABRA_BASICA = r"^[a-záéíóúñ]+$"
ER_PUNTUACION = r"^[.,;:¿?¡!]$"
ER_DIGITO = r"^\d+$"

# ------------------------------
# Cargar diccionario
# ------------------------------
def cargar_diccionario_csv(ruta_csv):
    try:
        df = pd.read_csv(ruta_csv)

        palabras_frecuencia = df['Frecuencia'].astype(str).str.lower()
        palabras_alfabetico = df['Alfabético'].astype(str).str.lower()

        diccionario = set(palabras_frecuencia) | set(palabras_alfabetico)

        return diccionario
    except Exception as e:
        st.error(f"Error cargando CSV: {e}")
        return set()

# ------------------------------
# Analizador léxico
# ------------------------------
def analizar_texto(texto_entrada, diccionario_validas):
    texto_entrada = texto_entrada.lower()

    # Separar puntuación con espacios
    texto_separado = re.sub(r'([.,;:¿?¡!])', r' \1 ', texto_entrada)

    palabras = texto_separado.split()
    resultados = []

    for lexema in palabras:
        if lexema in diccionario_validas:
            tipo = "PALABRA_VALIDA_ESPANOL"
        elif re.match(ER_PUNTUACION, lexema):
            tipo = "PUNTUACION"
        elif re.match(ER_DIGITO, lexema):
            tipo = "DIGITO"
        else:
            tipo = "ERROR_ORTOGRAFICO"
        
        resultados.append((tipo, lexema))

    return resultados


# ==============================
# 🚀 STREAMLIT APP
# ==============================
st.title("🔎 Analizador Léxico en Español")
st.write("Proyecto Final - Lenguajes y Autómatas II")

st.divider()

# Cargar diccionario una sola vez
ruta_csv = "/Users/limberg/Documents/ALL_Cuatrimestres/7mo-Cuatrimestre/lenguajes-y-automatas/proyecto-final-2/diccionario_español.csv"
diccionario = cargar_diccionario_csv(ruta_csv)

# Input del usuario
texto_usuario = st.text_area("✏️ Escribe una oración para analizar:", height=120)

if st.button("Analizar"):
    if texto_usuario.strip() == "":
        st.warning("⚠️ Ingresa una oración para analizar.")
    else:
        tokens = analizar_texto(texto_usuario, diccionario)

        st.subheader("📌 Resultado del análisis:")
        
        # Mostrar estilo tipo consola
        st.code("\n".join([f"{tipo:25} | {lexema}" for tipo, lexema in tokens]), language="text")

        # Mostrar en tabla también
        df_result = pd.DataFrame(tokens, columns=["Token", "Lexema"])
        st.table(df_result)

st.divider()
st.caption("UP Chiapas · Proyecto Final · Lenguajes y Autómatas II")
