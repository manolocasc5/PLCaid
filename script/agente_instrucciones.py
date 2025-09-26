import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")

llm = ChatOpenAI(model_name="gpt-4", temperature=0.1, openai_api_key=api_key)

PROMPT_SYSTEM = """
Eres un experto en automatización de interfaces de usuario para PLC Siemens TIA Portal y sistemas Windows.
Tu objetivo es traducir una orden de usuario en una secuencia de acciones GUI (Graphical User Interface).

Basado en la siguiente orden del operador y la descripción del estado actual de la pantalla,
genera **SOLO Y EXCLUSIVAMENTE UN JSON** que represente los pasos a seguir.

**Descripción del estado actual de la pantalla (simulada y adaptable según el monitor_id):**
En el monitor 1, se muestra la pantalla de inicio de Windows con iconos de acceso directo. Se espera acceder a TIA Portal. Acciones posibles: 'doble clic en icono TIA Portal', 'abrir explorador de archivos para buscar TIA Portal'.
En el monitor 2, se muestra la ventana principal de Siemens TIA Portal abierta, con el árbol de proyecto visible, bloques de funciones, y un botón para 'cargar al dispositivo'. Acciones posibles: 'clic en bloque de función', 'clic en cargar', 'arrastrar y soltar'.
En un monitor genérico, se muestra una interfaz de software, posiblemente TIA Portal, en un estado intermedio de configuración. Evalúa cuidadosamente las acciones.

**Reglas para la generación del JSON:**
1.  **Formato de Salida**: Una lista de objetos JSON.
2.  **Estructura de Cada Paso**: Cada objeto de paso debe tener EXACTAMENTE dos claves:
    * `"step"`: Una cadena de texto que representa el nombre de un archivo de imagen (recorte de pantalla) para ese paso. Estos nombres deben ser secuenciales y descriptivos, como "i1.png", "i2.png", "i3.png", etc. Se asume que estas imágenes existen o se generarán.
    * `"action"`: Una cadena de texto que indica la acción a realizar. Los ÚNICOS valores permitidos son: `"clic"` o `"texto"`.
3.  **Campo Adicional para 'texto'**: **IMPORTANTE**: Para la acción "texto", el JSON NO DEBE incluir un campo "value". El texto a escribir será determinado por otro módulo (`generador_scl.py`) más adelante en el flujo de ejecución.
4.  **No explicaciones**: No incluyas ninguna explicación, texto adicional, comentarios, o formato de markdown aparte del JSON. Tu respuesta debe ser el JSON puro y nada más.

**Ejemplo del Formato Deseado:**
```json
[
  { "step": "i1.png", "action": "clic" },
  { "step": "i2.png", "action": "texto" },
  { "step": "i3.png", "action": "clic" }
]
"""

def generar_json_desde_orden(orden: str, monitor_id: int = 1):
    print(f"DEBUG Agente: Función generar_json_desde_orden iniciada con orden: '{orden[:50]}...' y monitor: {monitor_id}")

    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template="{format_instructions}\n{system_prompt}\nOrden del operador: {orden_input}\nMonitor seleccionado: {monitor_id_input}\n",
        input_variables=["orden_input", "monitor_id_input"],
        partial_variables={"format_instructions": parser.get_format_instructions(), "system_prompt": PROMPT_SYSTEM}
    )

    chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)

    print("DEBUG Agente: Invocando la cadena LLM para generar JSON...")
    try:
        result_json = chain.invoke({
            "orden_input": orden,
            "monitor_id_input": monitor_id
        })

        print(f"DEBUG Agente: JSON generado y parseado (primeros 200 caracteres):\n{json.dumps(result_json, indent=2, ensure_ascii=False)[:200]}...")

        path = os.path.join("parsed_steps", "steps.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result_json, f, indent=2, ensure_ascii=False)
        print("DEBUG Agente: Archivo steps.json guardado correctamente.")
        
        return "steps.json generado y guardado exitosamente."

    except json.JSONDecodeError as e:
        try:
            raw_output = chain.invoke({"orden_input": orden, "monitor_id_input": monitor_id}, return_only_outputs=True)
        except Exception:
            raw_output = "No se pudo obtener la salida cruda del LLM."
        print(f"ERROR Agente: El LLM no generó un JSON válido: {e}. Output crudo: {raw_output}")
        raise ValueError(f"Fallo al generar JSON válido: {e}. Revisa el prompt y la capacidad del LLM.")
    except Exception as e:
        print(f"ERROR Agente: Fallo en la invocación de la cadena LLM o al guardar el archivo: {e}")
        raise