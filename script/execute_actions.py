import pyautogui
import time
import os
import pyperclip # Para manejar el portapapeles

# La pausa inicial se mantiene si es útil para el contexto general de la aplicación.
# time.sleep(2)

def action(step_image_name: str, action_type: str, text_content: str = None):
    """
    Realiza una acción (clic o escribir texto) en una imagen de la pantalla.
    
    Args:
        step_image_name (str): El nombre del archivo de imagen (ej. "i1.png") a localizar.
        action_type (str): El tipo de acción a realizar ("clic" o "texto").
        text_content (str, optional): El texto a escribir si action_type es "texto".
                                      Este parámetro se espera solo para acción "texto".
    """
    # Ruta a la imagen en la carpeta capture
    # Asumiendo que execute_actions.py está en 'script/', la raíz del proyecto es dos niveles arriba.
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(project_root, 'capture', step_image_name)

    print(f"Buscando imagen: {image_path} para realizar acción: {action_type}")

    location = None
    try:
        # Busca la imagen en pantalla.
        location = pyautogui.locateOnScreen(image_path, confidence=0.8, grayscale=False)
    except pyautogui.PyAutoGUIException as e:
        print(f"Error al buscar la imagen '{step_image_name}': {e}")
        raise # Re-lanzar para que main.py lo capture

    if location:
        center_x = location.left + location.width / 2
        center_y = location.top + location.height / 2
        print(f"Elemento '{step_image_name}' localizado en: ({center_x}, {center_y})")

        if action_type == "clic":
            pyautogui.click(center_x, center_y)
            print(f"Clic realizado en: {step_image_name}")
        elif action_type == "texto":
            if text_content is None:
                # Esto es crucial: Si action_type es "texto" y text_content es None,
                # significa que main.py no le pasó el texto.
                # Deberías considerar si esto es un error fatal o simplemente un paso que no hace nada.
                # Para este caso, lanzaremos un error, ya que para la acción "texto" siempre se espera un contenido.
                raise ValueError("La acción 'texto' requiere un contenido de texto para escribir.")
            
            # Hacer clic para asegurar que la ventana está activa y el cursor está donde debe.
            pyautogui.click(center_x, center_y) 
            time.sleep(0.1) # Pequeña pausa para asegurar el clic antes de pegar
            pyperclip.copy(text_content)  # Copia el texto al portapapeles
            pyautogui.hotkey('ctrl', 'v')  # Pega con Ctrl+V (en Mac usa 'command', 'v')
            print(f"Texto '{text_content[:50]}...' escrito en: {step_image_name}")
        else:
            print(f"Acción no reconocida: {action_type}. Ignorando paso.")
    else:
        raise RuntimeError(f"No se pudo localizar el elemento '{step_image_name}' en la pantalla actual con la confianza dada (0.8).")