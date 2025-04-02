from constants import INTENTS_JSON_PATH, INTENTS_TRAIN_JSON_PATH
from src.data_preprocessing import load_data
from src.intent_classifier import IntentClassifier

def train_classifier():
    """Entrenar el modelo desde cero o cargar el modelo entrenado previamente."""
    # Cargar los datos desde 'data/intents.json'
    data = load_data(INTENTS_JSON_PATH)

    # Crear una instancia del clasificador y entrenarlo
    classifier = IntentClassifier()

    # Entrenar el clasificador con los datos cargados
    classifier.train(data)

    # Devolver el clasificador entrenado
    return classifier


def retrain_classifier():
    """Reentrenar el modelo con nuevos datos."""
    # Cargar los nuevos datos desde 'data/intents.json'
    data = load_data(INTENTS_TRAIN_JSON_PATH)

    # Crear una instancia del clasificador
    classifier = IntentClassifier()

    # Reentrenar el clasificador con los datos cargados
    classifier.retrain(data)

    # Devolver el clasificador actualizado
    return classifier




# # Para interacción con el usuario desde consola
# while True:
#     user_input = input("Tú: ")
#     if user_input.lower() in ["salir", "exit"]:
#         print("Chatbot: ¡Hasta luego!")
#         break
#     intent = classifier.predict(user_input)
#     print(f"Chatbot: Identificado como la intención '{intent}'")
