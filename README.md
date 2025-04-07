# Machine Learning, clasificación de intenciones: ChatBot.
Este proyecto implementa un clasificador de intenciones utilizando el algoritmo Naive Bayes multinomial y el modelo de representación de texto TF-IDF para analizar el texto y predecir una "intención" asociada. Está diseñado como un proyecto educativo en el área de procesamiento de lenguaje natural (NLP) y aprendizaje automático.

## ¿Qué es la clasificación de intenciones?

La clasificación de intenciones es un proceso de Machine Learning donde el objetivo es identificar la intención o propósito detrás de la entrada del usuario. Las intenciones son las acciones que un usuario quiere realizar al interactuar con el chatbot.

Por ejemplo, si un usuario dice:
* "¿Cómo está el clima hoy?" → La intención es "consultar el clima".
* "Quiero saber mi saldo bancario" → La intención es "consultar saldo".

En un chatbot con clasificación de intenciones, el sistema toma el mensaje del usuario y lo clasifica en una de las categorías o intenciones predefinidas, lo que le permite generar una respuesta relevante.

### ¿Cómo funciona un chatbot de clasificación de intenciones?

El proceso básico de un chatbot basado en clasificación de intenciones sigue estos pasos:

1. Recolección de datos de entrenamiento: Para entrenar un modelo de Machine Learning, necesitas ejemplos de lo que los usuarios podrían decir (llamados "mensajes de entrenamiento") junto con las intenciones correspondientes (las categorías en las que deben clasificarse esos mensajes).
Ejemplo de datos de entrenamiento:
    * "¿Qué hora es?" → Intención: "consultar hora"
    * "Muéstrame los resultados del partido de fútbol" → Intención: "consultar resultados deportivos"

2. Preprocesamiento del texto: Antes de entrenar un modelo, los datos de texto generalmente deben preprocesarse. Esto puede incluir:

    * Tokenización: Separar el texto en palabras o subpalabras.

    * Eliminación de stopwords: Eliminar palabras comunes que no aportan significado relevante (como "y", "de", "el", etc.).

    * Lematización/Stemming: Reducir las palabras a su forma raíz (por ejemplo, "corriendo" → "correr").

    * Vectorización: Convertir el texto en una representación numérica, utilizando por ejemplo TF-IDF o Word Embeddings (como Word2Vec o GloVe).

3. Entrenamiento del modelo de Machine Learning: Una vez que los datos están preprocesados, puedes entrenar un modelo de Machine Learning para clasificar las intenciones. Algunos de los algoritmos más comunes para esta tarea incluyen:

    * Máquinas de soporte vectorial (SVM): Un clasificador eficiente para tareas de clasificación de texto.

    * Naive Bayes: Popular en tareas de clasificación de texto por su simplicidad y eficiencia.

    * Redes neuronales: Usadas cuando se dispone de grandes volúmenes de datos, como LSTM (Long Short Term Memory) o Transformers.

    * Modelos preentrenados: Como BERT o GPT, que se pueden ajustar (fine-tune) para tareas de clasificación de intenciones específicas.

4. Predicción de la intención: Cuando el usuario envía un mensaje, el chatbot usa el modelo entrenado para clasificar ese mensaje en una de las intenciones que aprendió durante el entrenamiento. Por ejemplo, si el usuario pregunta "¿Qué tal el clima?", el modelo podría clasificar este mensaje en la intención "consultar clima".

5. Generación de respuesta: Una vez que se identifica la intención, el chatbot puede generar una respuesta apropiada, ya sea utilizando una base de datos de respuestas predefinidas o generando una respuesta dinámica si está utilizando técnicas más avanzadas (como GPT).

## Descripción.

El proyecto permite que un chatbot clasifique las intenciones de un mensaje de texto proporcionado por el usuario. Utiliza un modelo de clasificación entrenado previamente que puede ser cargado o actualizado a medida que se ingresan nuevos datos utilizando archivos Json. 

Este proyecto utilizó la implementación del clasificador Naive Bayes para datos multinomiales de `scikit-learn`, que es muy adecuado para problemas de clasificación de texto. El clasificador funciona bajo la suposición de que las características (en este caso, las palabras en los textos) son independientes entre sí, lo que permite calcular probabilidades condicionales de manera eficiente. También se utiliza un transformador que convierte un conjunto de documentos de texto en una matriz de características numéricas, utilizando la técnica TF-IDF (Term Frequency-Inverse Document Frequency) de `scikit-learn`. Esta técnica ayuda a ponderar la importancia de las palabras en un conjunto de documentos.
Además, se utiliza el método `make_pipeline` de `scikit-learn` que facilita la creación de un pipeline, que en este caso conecta el transformador TfidfVectorizer con el clasificador MultinomialNB. El pipeline permite que el flujo de datos se maneje de manera eficiente y escalable. Esto sucede al automatizar y organiza el proceso de modelado para que cada paso no tenga que ejecutarse manualmente, es decir, lo que hace el pipeline es encadenar estos dos pasos, lo que significa que al llamar a fit() o predict() en el modelo, primero se realiza la transformación (TF-IDF) y luego se aplica el modelo de clasificación (Naive Bayes) a la representación numérica generada.

## Requisitos.

Este proyecto fue desarrollado utilizando Python 3.13.0 y un entorno virtual. Asegúrate de tener instaladas las siguientes librerías y sus dependencias antes de ejecutar el proyecto:

- flet
- joblib
- scikit-learn

### Crea y activa un entorno virtual.
Navega al directorio del proyecto:
```bash
    cd chatbot-ML-classification-intentions
```
Crea y activa un entorno virtual:
```bash
    python3 -m venv venv
    source venv/bin/activate  # Para sistemas Unix
    venv\Scripts\activate     # Para sistemas Windows
```

### Instala todas las librerias necesarias.
Navega al directorio del proyecto:
```bash
    cd chatbot-ML-classification-intentions
```
```bash
    pip install -r requirements.txt
```
## Entorno de Desarrollo

El proyecto fue desarrollado y probado en **Visual Studio Code (VSCode)**, utilizando las siguientes herramientas y extensiones.

- **Jupyter Extension for Visual Studio Code, de Microsoft** contiene 4 paquetes de extensión: Jupyter Keymap, Jupyter Notebook Renderers, Jupyter Slide Show y Jupyter Cell Tag.
- **Jupyter PowerToys, de Microsoft** Proporciona características experimentales para extender la experiencia del cuaderno de Jupyter en VS Code.
- **Python, de Microsoft** 
    - **Python Debugger, de Microsoft** Proporciona una experiencia de depuración fluida permitiándole establecer puntos de interrupción, pasar el código, inspeccionar variables y realizar otras tareas esenciales de depuración. 
    - **Pylance, de Microsoft** Para mejorar la inteligencia de código y la depuración en Python.

## Uso.

Navega al directorio del proyecto:
```bash
    cd chatbot-ML-classification-intentions
```
Para ejecutar el chatbot, simplemente ejecuta el siguiente comando:
```bash
    python src/ui/gui_flet.py
```
Esto iniciará la interfaz gráfica del chatbot. Al ingresar el primer mensaje, el sistema buscará cargar un modelo ya entrenado (si existe). Si no existe, se entrenará un modelo nuevo utilizando los datos de intents.json y luego se procederá a clasificar la intención del mensaje.

## Flujo del Proyecto.
El flujo del proyecto es el siguiente:

1. **Interfaz de usuario (UI)**: El archivo `gui_flet.py` proporciona la interfaz gráfica de usuario utilizando la librería `flet`, que recibe el mensaje del usuario.
2. **Procesamiento del mensaje**: El mensaje se envía al archivo `chatbot.py`, donde se procesa. Si es el primer mensaje, se inicializa el modelo.
3. **Inicialización o carga del modelo**: En el archivo `intent_classifier_model.py`, el modelo de clasificación se carga si ya existe en la carpeta `models`. Si no existe, se crea un nuevo modelo y se entrena utilizando los datos de `intents.json` en la carpeta `data`.
4. **Entrenamiento y actualización**: Si se encuentra un archivo de entrenamiento en la carpeta `data`, se carga y actualiza el modelo, creando un nuevo archivo y moviendo los archivos antiguos a carpetas de respaldo.
5. **Predicción**: Una vez cargado el modelo, se realiza la predicción de la intención del mensaje del usuario y se busca la respuesta asociada en el archivo `intents.json`.
6. **Actualización continua**: Cada vez que se ejecuta el archivo `gui_flet.py`, el modelo puede ser reentrenado con los datos nuevos de `intents_train.json`, lo que permite que el modelo mejore con el tiempo.

## Archivos importantes.

* intents.json: Archivo que contiene las intenciones y ejemplos asociados a cada intención.
* intents_train.json: Archivo que contiene datos de entrenamiento adicionales para mejorar el modelo.
* Modelos: Los modelos entrenados se guardan como archivos .pkl en la carpeta models.

### Archivo intents.json.
El archivo intents.json define las intenciones base del chatbot, con ejemplos de frases para cada intención y las respuestas asociadas. A continuación se muestra un template básico de este archivo:
```bash
    {
        "intents": [
            {
                "intent": "Nombre_de_la_intención",
                "examples": [
                    "Ejemplo 1",
                    "Ejemplo 2",
                    "Ejemplo 3"
                ],
                "response": "Respuesta asociada a la intención."
            },
            {
                "intent": "Otra_intención",
                "examples": [
                    "Otro ejemplo 1",
                    "Otro ejemplo 2"
                ],
                "response": "Respuesta asociada a esta otra intención."
            }
        ]
    }
```

### Archivo intents_train.json.
El archivo intents_train.json define las nuevas intenciones que se desean incorporarlas a las antiguas y reentrenar el modelo que usa el Chatbot con una base más grande de intenciones. A continuación se muestra un template básico de este archivo:

```bash
    {
        "intents": [
            {
                "intent": "Nombre_de_la_intención",
                "examples": [
                    "Ejemplo 1",
                    "Ejemplo 2",
                    "Ejemplo 3"
                ],
                "response": "Respuesta asociada a la intención."
            },
            {
                "intent": "Otra_intención",
                "examples": [
                    "Otro ejemplo 1",
                    "Otro ejemplo 2"
                ],
                "response": "Respuesta asociada a esta otra intención."
            }
        ]
    }
```
En la carpeta `examples/` se encuentran ejemplos de estos archivos.