'''
implementa un clasificador de intenciones utilizando el algoritmo Naive Bayes multinomial y el modelo de 
representación de texto TF-IDF para analizar el texto y predecir una "intención" asociada. 
'''


'''
implementación del clasificador Naive Bayes para datos multinomiales, que es muy adecuado para problemas 
de clasificación de texto. El clasificador funciona bajo la suposición de que las características (en este caso, 
las palabras en los textos) son independientes entre sí, lo que permite calcular probabilidades condicionales 
de manera eficiente.
'''
from sklearn.naive_bayes import MultinomialNB
'''
es un transformador que convierte un conjunto de documentos de texto en una matriz de características numéricas, 
utilizando la técnica TF-IDF (Term Frequency-Inverse Document Frequency). Esta técnica ayuda a ponderar la 
importancia de las palabras en un conjunto de documentos.
'''
from sklearn.feature_extraction.text import TfidfVectorizer
'''
método de sklearn que facilita la creación de un pipeline, que en este caso conecta el transformador 
TfidfVectorizer con el clasificador MultinomialNB. El pipeline permite que el flujo de datos se maneje 
de manera eficiente y escalable.
'''
from sklearn.pipeline import make_pipeline
'''
Este módulo se utiliza para trabajar con datos en formato JSON
'''
from constants import MODELS_PATH


import json

import joblib
from datetime import datetime
import os


class IntentClassifier:
    def __init__(self, model_filename=None):
        # Si no se pasa un modelo, verificamos si ya existe uno guardado
        if model_filename is None:
            self.model_filename = self.get_most_recent_model()
            if not self.model_filename:  # Si no existe un modelo guardado
                # Si no existe modelo, se crea un nuevo modelo
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                self.model_filename = f"{MODELS_PATH}/modelo_entrenado_{timestamp}.pkl"
                self.model = self.create_new_model()
                print("No se encontró un modelo guardado. Creando uno nuevo.")
        else:
            self.model_filename = model_filename
            self.model = self.load_model(self.model_filename)
        
        # Aseguramos que la carpeta 'models' exista
        os.makedirs(os.path.dirname(self.model_filename), exist_ok=True)


    def create_new_model(self):
        """Crea un nuevo modelo desde cero."""
        # Pipeline es un flujo de trabajo estructurado que automatiza y organiza el proceso de modelado, 
        # para que no sea necesario ejecutar manualmente cada paso.
        # Lo que hace el pipeline es encadenar estos dos pasos, lo que significa que cuando llamas a fit() o 
        # predict() en el modelo, primero se realiza la transformación (TF-IDF) y luego se aplica el modelo 
        # de clasificación (Naive Bayes) en la representación numérica generada.
        return make_pipeline(TfidfVectorizer(), MultinomialNB())


    def get_most_recent_model(self):
        """Verifica si hay modelos guardados y devuelve el más reciente."""
        #models_dir = 'models'
        try:
            # Listamos todos los archivos .pkl en el directorio models
            model_files = [f for f in os.listdir(MODELS_PATH) if f.endswith('.pkl')]
            if not model_files:
                return None  # No hay modelos guardados
            # Ordenamos los archivos por fecha de modificación
            model_files.sort(key=lambda x: os.path.getmtime(os.path.join(MODELS_PATH, x)), reverse=True)
            return os.path.join(MODELS_PATH, model_files[0])  # Devuelve el más reciente
        except FileNotFoundError:
            return None  # Si no existe la carpeta 'models'


    def load_model(self, filename):
        """Carga un modelo entrenado desde un archivo."""
        try:
            model = joblib.load(filename)
            print(f"Modelo cargado desde {filename}")
        except FileNotFoundError:
            print(f"No se encontró el modelo en {filename}. Creando un modelo nuevo.")
            model = self.create_new_model()
        return model


    def save_model(self):
        """Guarda el modelo entrenado en un archivo."""
        joblib.dump(self.model, self.model_filename)
        print(f"Modelo guardado en {self.model_filename}")


    def train(self, data):        
        # Lista para almacenar ejemplos de texto, es decir, las entradas de texto que se 
        # usarán para entrenar el modelo.
        X_train = []  
        # Lista para almacenar las intenciones correspondientes. Estas intenciones son las 
        # etiquetas que el modelo debe aprender a predecir.
        y_train = []  
        
        # Iterar sobre cada intención en los datos
        for intent_data in data['intents']:
            # Extraer ejemplos (textos de entrenamiento) y la intención correspondiente
            examples = intent_data['examples']
            intent = intent_data['intent']
            
            # Agregar los ejemplos a X_train y las intenciones a y_train
            for example in examples:
                X_train.append(example)
                y_train.append(intent)

        # entrena el modelo (self.model) utilizando los datos de entrenamiento (X_train y y_train). 
        # El modelo aprenderá a mapear los textos a sus correspondientes intenciones.
        self.model.fit(X_train, y_train)

    # Este método recibe un mensaje de texto (message) como entrada y utiliza el modelo entrenado para 
    # predecir la intención asociada con ese mensaje.
    def predict(self, message):
        # La función predict() recibe un arreglo de textos (por lo que el mensaje debe ser envuelto en una lista). 
        # El modelo realiza la predicción y devuelve una lista de intenciones predichas.
        # Como solo se pasa un único mensaje (y por lo tanto solo se generará una predicción), se selecciona el 
        # primer (y único) valor de la lista de predicciones, que es la intención predicha para el mensaje.
        return self.model.predict([message])[0]
