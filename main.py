import os
import json
import time

from script.execute_actions import action
from script.generador_scl import codificar_scl
from script.agente_instrucciones import generar_json_desde_orden

# Ruta base del proyecto
project_root = os.path.dirname(os.path.abspath(__file__))

print("DEBUG: main.py iniciado.")

# Leer orden del archivo
order_path = os.path.join(project_root, "input_text", "order.txt")
try:
    with open(order_path, "r", encoding="utf-8") as f:
        order = f.read()
    print(f"DEBUG: Orden '{order.strip()}' leída de {order_path}")
except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo de orden en {order_path}")
    exit(1)

# Leer MONITOR_ID de la variable de entorno
monitor_id = int(os.getenv("MONITOR_ID", "1")) # Por defecto, usa el monitor 1 (primario)
print(f"DEBUG: MONITOR_ID recibido: {monitor_id}")

# Ejecutar agente para generar steps.json
print("DEBUG: Llamando a generar_json_desde_orden...")
try:
    generar_json_desde_orden(order, monitor_id)
    print("DEBUG: generar_json_desde_orden completado.")
except Exception as e:
    print(f"ERROR: Fallo al generar JSON de pasos: {e}")
    exit(1) # Salir si el agente falla

# Leer y ejecutar los pasos
steps_json_path = os.path.join(project_root, "parsed_steps", "steps.json")
try:
    with open(steps_json_path, "r", encoding="utf-8") as f:
        raw_steps_data = json.load(f) # Cargar todo el diccionario
    
    # --- CAMBIO CRUCIAL AQUÍ ---
    # Acceder a la lista de pasos a través de la clave 'text'
    if isinstance(raw_steps_data, dict) and "text" in raw_steps_data:
        steps = raw_steps_data["text"]
    else:
        # Si por alguna razón no es un dict o no tiene 'text', intentamos cargarlo directo
        # Esto es un fallback, lo ideal es que siempre venga en "text"
        steps = raw_steps_data
        print("ADVERTENCIA: El JSON de pasos no contiene la clave 'text'. Asumiendo que el JSON es directamente la lista.")


    print(f"DEBUG: {len(steps)} pasos cargados de {steps_json_path}")
except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo de pasos en {steps_json_path}. El agente puede haber fallado o la ruta es incorrecta.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"ERROR: Error al parsear steps.json: {e}")
    exit(1)


total_steps = len(steps)
num_step = 0

print(f"DEBUG: Iniciando ejecución de {total_steps} pasos...")
while num_step < total_steps:
    step_data = steps[num_step]
    step_image_name = step_data.get("step", "N/A")
    step_action_type = step_data.get("action", "N/A")

    print(f"DEBUG: Ejecutando paso {num_step + 1}/{total_steps}: Imagen='{step_image_name}', Acción='{step_action_type}'")

    try:
        if step_action_type == "texto":
            print("DEBUG: Generando código SCL...")
            codigo_scl = codificar_scl(order) # Usar la orden original para generar el SCL
            print(f"DEBUG: Código SCL generado (primeras 50 chars):\n{codigo_scl[:50]}...") # Mostrar solo el inicio
            action(step_image_name, step_action_type, codigo_scl) # Pasar codigo_scl como text_content
        else: # "clic"
            action(step_image_name, step_action_type)
        print(f"DEBUG: Paso {num_step + 1} completado.")
        num_step += 1
        time.sleep(1) # Pequeña pausa entre pasos para estabilidad
    except Exception as e:
        print(f"ERROR en paso {num_step + 1} (Imagen: {step_image_name}, Acción: {step_action_type}): {e}")
        print("DEBUG: Reintentando en 5 segundos...")
        time.sleep(5)

print("\n✅ Flujo completo ejecutado.")