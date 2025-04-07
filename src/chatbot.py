from src.intent_classifier_model import IntentClassifier

# Global variable to store the classifier
classifier = None


# Obtain a trained classifier model or train a new one if one does not exist
def get_or_train_classifier():
    
    global classifier
    try:
        if classifier is None:
            print("Cargando el modelo...")
            # Initializes the classifier
            classifier = IntentClassifier()  
            # If a model cannot be loaded, whether it is a saved one or a created one
            if not classifier.model:
                print("Se genero un error y no fue posible cargar un Modelo o crearlo")
                return None
        return classifier
    except Exception as e:
        # Catch any other unexpected errors related to classifier initialization
        print(f"Error al cargar o crear el clasificador: {e}")
        return None


# Receives the user's message and returns the response generated by the classifier.
def process_message(user_input):    
    try:
        # Gets the classifier if it is not already loaded
        classifier = get_or_train_classifier()
        if classifier is None:
            raise ("No se pudo cargar el clasificador.")
        # Classify the intention of the message
        intent = classifier.predict(user_input)
        # Find the answer corresponding to the intention
        response = classifier.response_message_to_intent(intent)
        # returns the response
        return response
    except Exception as e:
        # Catch any unexpected errors during the message processing
        raise Exception(f"{e}")
