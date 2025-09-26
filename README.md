# PLCaid: Agente de Automatización y Generación de Código SCL

## 💡 Descripción del Proyecto

**PLCaid** es un prototipo de agente de inteligencia artificial diseñado para automatizar la configuración de entornos de PLC y generar código de control en lenguaje SCL (Structured Control Language) basado en instrucciones dadas en lenguaje natural.

El objetivo es simplificar flujos de trabajo complejos de automatización industrial, como la configuración de TIA Portal, utilizando visión por computadora, bases de datos vectoriales y modelos de lenguaje grande.

## ⚙️ Arquitectura de la Implementación Actual

El proyecto opera bajo un flujo de trabajo **secuencial** que combina dos estrategias de localización de UI:

1.  **Entrada del Usuario:** El usuario introduce una orden por texto o voz a través de la interfaz web de Streamlit.
2.  **Fase de Navegación Flexible (`steps.json`):** El sistema traduce descripciones de texto (`"Abrir la vista del proyecto"`) a vectores (embeddings) y los busca en **Qdrant** para encontrar la imagen de UI más relevante.
3.  **Generación de Código:** La orden del usuario se envía a la API de **OpenAI (GPT-4)**, que genera el código SCL optimizado para PLC/HMI.
4.  **Fase de Ejecución de Código y Finalización (`steps2.json`):** El sistema utiliza rutas de imagen fijas (`../capture/i8.png`) y **PyAutoGUI** para pegar el código SCL en la interfaz y completar los pasos finales (compilar, guardar).

---

## 📦 Estructura del proyecto

```bash
project-root/
│
├── input/                   # Entradas manuales: texto o voz
│   ├── text_orders/         # Archivos de texto con órdenes
│   └── voice_clips/         # Audios a transcribir (WAV, MP3)
│
├── parsed_steps/           # JSONs con pasos desglosados desde input
│
├── screenshots/            # Capturas de pantalla tomadas manual o automáticamente
│
├── vision_outputs/         # Output de GPT Vision: coordenadas o instrucciones por imagen
│
├── executions/             # Capturas después de ejecutar acciones
│
├── scripts/                # Todos los módulos funcionales
│   ├── text_to_steps.py
│   ├── voice_to_text.py
│   ├── screenshot.py
│   ├── vision_prompt.py
│   ├── execute_actions.py
│   └── orchestrate.py
│
├── README.md
└── requirements.txt
```

## 🚀 Visión y Futuras Implementaciones

Para transformar PLCaid en un agente autónomo y robusto, la hoja de ruta incluye la adopción de arquitecturas de agentes avanzadas y la migración de tareas a modelos locales.

### 1. Arquitectura Multiagente (LangGraph)

* **Implementación:** Utilizar un *framework* como **LangGraph** para orquestar agentes especializados.
* **Valor Añadido:** El sistema pasará de un guion lineal a un flujo dinámico, permitiendo el **manejo inteligente de errores** y la **recuperación autónoma** si un elemento de UI cambia o no aparece.

### 2. Migración a LLMs Multimodales y Locales

* **LLMs Multimodales:** Integrar modelos avanzados (GPT-4o / Gemini 1.5 Pro) para un **razonamiento visual** más profundo, permitiendo al agente comprender el contexto de la UI en su totalidad (no solo buscando un elemento específico).
* **Uso Local:** Evaluar el uso de modelos pequeños y eficientes (e.g., LLaMA 3, Mistral) en local para reducir la latencia, los costos y la dependencia de APIs externas.

### 3. Integración de OCR y RAG

* **Herramientas de OCR (con OpenCV):** Utilizar **OpenCV** y motores de OCR (como Tesseract) para mejorar la **fiabilidad en la lectura de texto pequeño** en la UI, como etiquetas y mensajes de error, complementando al LLM.
* **RAG (Generación Aumentada con Recuperación):** Extender el uso de **Qdrant** para indexar manuales y documentación de PLC. Esto permitirá que el agente genere código SCL con información actualizada, superando las limitaciones de la fecha de corte de entrenamiento de los LLMs.

---

## ⚙️ Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone [URL_DEL_REPOSITORIO]
    cd PLCaid
    ```

2.  **Crear y activar el entorno virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Linux/macOS
    .\.venv\Scripts\activate  # En Windows
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Crea un archivo llamado **`.env`** en la raíz del proyecto y añade tus claves de API y configuraciones de Qdrant:
    ```env
    OPENAI_API_KEY="sk-..."
    GEMINI_API_KEY="AIza..."
    QDRANT_URL="[Tu URL de Qdrant o 'localhost']"
    QDRANT_API_KEY="[Tu clave de Qdrant si usas la nube]"
    COLLECTION_NAME="plc_ui_vectors"
    ```

5.  **Indexar las imágenes:**
    Ejecuta el script de indexación para llenar la base de datos de Qdrant con los embeddings de las capturas de UI:
    ```bash
    python image_indexer.py
    ```

---

## 🚀 Ejecución del Proyecto

Para iniciar la interfaz de usuario:

```bash
streamlit run interface.py
```

Una vez iniciada la interfaz, puedes escribir o grabar una orden en lenguaje natural y seleccionar el monitor donde se encuentra el entorno de PLC activo.

## 📄 Licencia
MIT – Uso libre para fines de desarrollo, estudio y mejora de automatización con visión + LLM.

## 👥 Equipo
Proyecto desarrollado por 3 integrantes en 2 semanas. Cada módulo fue testeado individualmente y luego integrado paso a paso.

