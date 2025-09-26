import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la API key en el archivo .env")

# Inicializar cliente OpenAI
client = OpenAI(api_key=api_key)

def codificar_scl(texto: str):
    # Pedir input al usuario
    orden = texto

    # Construir el prompt
    prompt = f"""
Eres un experto programador de PLC Siemens S7-1200.
Dado el siguiente requerimiento en lenguaje natural, genera el código en lenguaje SCL necesario para implementarlo.

Requerimiento: "{orden}"

Formato de salida: Solo y exclusivamente el código SCL, sin explicaciones ni comentarios. Y sólo el código a partir del 
primer if hasta el final del código completo, incluyendo en la última línea la variable Q_Motor y su estado.

Nombre de variables:
"MarchaParo_1"(
               Start := "Tag_1",         // Pulsador de marcha
               Stop := "Tag_2",          // Pulsador de paro
               Q_Motor => "Tag_3"        // Salida al motor
);
"""

    # Solicitar la respuesta al modelo
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        codigo_scl = response.choices[0].message.content
        return codigo_scl

    except Exception as e:
        print(f"Ocurrió un error al generar el código SCL: {e}")
