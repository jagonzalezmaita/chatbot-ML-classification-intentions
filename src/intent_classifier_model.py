'''
Implementation of an intent classifier using the multinomial Naive Bayes algorithm and the 
TF-IDF text representation model to analyze text and predict an associated intent.
'''

import os
import joblib
from datetime import datetime, timedelta

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from constants import MODELS_PATH, INTENTS_JSON_PATH, DATA_PATH, OLD_TRAIN_FILES_PATH
from constants import OLD_INTENTS_FILES_PATH, INTENTS_JSON, INTENTS_TRAIN_JSON
from src.utils import load_data, save_json, add_intents, validate_json_structure, move_and_rename_file


class IntentClassifier:
    
    # Constructor. Load a stored model if available or create and train a new model, then load it.
    def __init__(self):
        try:
            # Get the most recent model or None if no models exist
            self.model_filename = self.get_most_recent_model()
            if not self.model_filename:  # If no saved model exists
                # If no model exists, create a new one
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                self.model_filename = f"{MODELS_PATH}/trained_model_{timestamp}.pkl"
                self.model = self.create_new_model()
                data = load_data(INTENTS_JSON_PATH)
                self.train(data)
                self.save_model()
                print(f"No se encontró un modelo guardado. Se creo uno nuevo en {self.model_filename}.")
            else:
                self.model=self.load_model(self.model_filename)
            
            # Check if there are training files to retrain the model
            train_file = self.get_train_file()
            if train_file:  # If there is a training file saved
                train_data= load_data (train_file)
                print(f"Se encontró un archivo de entrenamiento: {train_file}")
                # Validate if the training file has the correct format
                if validate_json_structure(train_data):
                    # The date is obtained to incorporate into the file backups
                    timestamp = (datetime.now()+ timedelta(seconds=1)).strftime("%Y-%m-%d_%H-%M-%S")
                    # Use to copy the intents and examples to the intent.json file
                    intents_data = load_data(INTENTS_JSON_PATH)
                    # Update intents with new data
                    updated_data = add_intents(intents_data, train_data)
                    # Move the training file to archive
                    move_and_rename_file(train_file,
                                            f"{timestamp}_{INTENTS_TRAIN_JSON}",
                                            OLD_TRAIN_FILES_PATH) 
                    # Archive the intents file
                    move_and_rename_file(INTENTS_JSON_PATH,
                                            f"{timestamp}_{INTENTS_JSON}",
                                            OLD_INTENTS_FILES_PATH)
                    # Save the updated intents file
                    save_json(updated_data, INTENTS_JSON_PATH)
                    print(f"Archivo intents actualizado con éxito en: {INTENTS_JSON_PATH}")
                    # Retrain the model with updated data
                    self.train(updated_data)
                    print(f"Se re-entrenó el modelo actual: {self.model_filename}")            
                    # se modifica el nombre del nuevo archivo del modelo que acaba de ser entrenado
                    self.model_filename = f"{MODELS_PATH}/trained_model_{timestamp}.pkl"
                    # Save the new retrained model
                    self.save_model()
                    # Load the new retrained model
                    self.model=self.load_model(self.model_filename)
                else:
                    print(
                            f"La estructura del archivo train, no es válida."
                            f"\nSe mantiene el modelo actual: {self.model_filename}"
                        )
        except Exception as e:
            raise Exception(f"Error al inicializar el clasificador: {e}")


    # Creates a new model
    def create_new_model(self):        
        try:
            # Pipeline is a structured workflow that automates and organizes the modeling process so 
            # that each step doesn't need to be executed manually.
            # What the pipeline does is chain these two steps together, meaning that when you call 
            # fit() or predict() on the model, the transformation (TF-IDF) is performed first, and 
            # then the classification model (Naive Bayes) is applied to the generated numerical 
            # representation.
            return make_pipeline(TfidfVectorizer(), MultinomialNB())
        except Exception as e:
            raise Exception(f"Error al crear el modelo: {e}")


    # Gets the most recent model from the models directory
    def get_most_recent_model(self):        
        try:
            # List all .pkl files in the models directory
            model_files = [f for f in os.listdir(MODELS_PATH) if f.endswith('.pkl')]
            if not model_files:
                return None  # No models saved
            # Sort files by modification time and return the most recent
            model_files.sort(key=lambda x: os.path.getmtime(os.path.join(MODELS_PATH, x)), reverse=True)
            return os.path.join(MODELS_PATH, model_files[0])  # Return the most recent
        except FileNotFoundError as e:
            print(f"Error: No se encontró el directorio de datos. {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener el modelo más reciente: {e}")
            return None


    # Loads a trained model from a file
    def load_model(self, filename): 
        try:
            model = joblib.load(filename)
            print(f"Modelo cargado desde {filename}")
            return model
        except Exception as e:
            raise Exception(f"Error al cargar el modelo desde {filename}: {e}")


    # Saves the model to a file
    def save_model(self):
        try:
            joblib.dump(self.model, self.model_filename)
            #print(f"Modelo guardado en {self.model_filename}")
        except Exception as e:
            raise Exception(f"Error al guardar el modelo en {self.model_filename}: {e}")


    # Gets the most recent training file to retrain the model if exist
    def get_train_file(self):        
        try:
            # We list all the training files in the data directory
            train_files = [f for f in os.listdir(DATA_PATH) if f == INTENTS_TRAIN_JSON]
            if not train_files:
                return None  # No training file saved
            # Sort files by modification time and return the most recent
            train_files.sort(key=lambda x: os.path.getmtime(os.path.join(DATA_PATH, x)), reverse=True)
            return os.path.join(DATA_PATH, train_files[0])  # Return the most recent
        except FileNotFoundError as e:
            print(f"Error: No se encontró el directorio de datos. {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al buscar si hay archivos para entrenar el modelo: {e}")
            return None


    # Trains the model with the given data
    def train(self, data):
        try:
            # List to save text examples, the text inputs that will be used to train the model.
            X_train = []  
            # List to save the corresponding intents. These intents are the # labels that the model 
            # must learn to predict.
            y_train = []
            # Iterate over each intent in the data
            for intent_data in data['intents']:
                # Extract examples (training texts) and the corresponding intention
                examples = intent_data['examples']
                intent = intent_data['intent']                
                # Add the examples to X_train and the intentions to y_train
                for example in examples:
                    X_train.append(example)
                    y_train.append(intent)
            # train the model (self.model) using the training data (X_train and y_train).
            # The model will learn to map texts to their corresponding intents.
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise Exception(f"Error al entrenar el modelo: {e}")


    # Receives a text message as input and uses the trained model to predict the intent associated 
    # with that message.
    def predict(self, message):
        try:
            # The model performs the prediction and returns a list of predicted intents, but
            # since only one message is passed (and therefore only one prediction will be generated), 
            # the first (and only) value from the list of predictions is selected, which is the 
            # predicted intent for the message.
            return self.model.predict([message])[0]
        except Exception as e:
            raise Exception(f"Error al predecir la intención del mensaje: {e}")


    # Returns the response corresponding to the intent
    def response_message_to_intent(self, intent):
        try:
            data = load_data(INTENTS_JSON_PATH)        
            # Create a dictionary to quickly search for answers
            intent_map = {item['intent']: item['response'] for item in data['intents']}
            # Find the answer corresponding to the intent
            response = intent_map.get(intent)        
            if response:
                return response
            else:
                # If the intent is not found, throw a custom exception
                raise Exception(
                                    f"Lo siento, el intent '{intent}' no existe en el archivo JSON, "
                                    f"debe actulizar el archivo correspondiente al modelo usado."
                                )
        except Exception as e:
            raise Exception(f"Error al obtener la respuesta para el intent '{intent}': {e}")