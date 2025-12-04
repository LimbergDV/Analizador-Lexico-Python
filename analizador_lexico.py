import pandas as pd
import re # Necesario para separar puntuación y regex rápidas

# Definimos las expresiones regulares (Ajustadas ligeramente)
ER_PALABRA_BASICA = r"^[a-záéíóúñ]+$"
ER_PUNTUACION = r"^[.,;:¿?¡!]$" 
ER_DIGITO = r"^\d+$"

def cargar_diccionario_csv(ruta_csv):
    try:
        df = pd.read_csv(ruta_csv)
        
        # Convertimos a string y minúsculas para asegurar consistencia
        palabras_frecuencia = df['Frecuencia'].astype(str).str.lower()
        palabras_alfabetico = df['Alfabético'].astype(str).str.lower()
        
        # Unimos en un SET (conjunto) para búsqueda O(1)
        diccionario = set(palabras_frecuencia) | set(palabras_alfabetico)
        
        print(f"Total palabras en diccionario: {len(diccionario)}")
        return diccionario
    except Exception as e:
        print(f"Error cargando CSV: {e}")
        return set()

def analizar_texto(texto_entrada, diccionario_validas):
    # Normalizamos a minúsculas
    texto_entrada = texto_entrada.lower()
    
    # Truco de regex: Agrega espacios alrededor de la puntuación para que split() funcione bien
    # Ejemplo: "hola," se convierte en "hola ,"
    texto_separado = re.sub(r'([.,;:¿?¡!])', r' \1 ', texto_entrada)
    
    palabras = texto_separado.split()
    resultados = []

    for lexema in palabras:
        tipo = ""
        
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

ruta_csv = "/Users/limberg/Documents/ALL_Cuatrimestres/7mo-Cuatrimestre/lenguajes-y-automatas/proyecto-final-2/diccionario_español.csv" 
diccionario = cargar_diccionario_csv(ruta_csv)

texto_prueba = "El perro corrio 3 veses acia la kasa. ¿tenemos computadoras?"

tokens = analizar_texto(texto_prueba, diccionario)

print(f"{'Token':<30} | {'Lexema'}")
print("-" * 45)
for tipo, valor in tokens:
    print(f"{tipo:<30} | {valor}")