import json
import os

# Load a JSON file and return dictionary with data from a JSON file
def load_data(file_path):    
    try:
        # Attempt to open the file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            # Attempt to load the JSON data from the file
            data = json.load(f)
            return data
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"Error: The file '{file_path}' was not found.")
        raise  # Re-raise the exception for further handling if needed
    except json.JSONDecodeError as e:
        # Handle the case where the file content is not valid JSON
        print(f"Error: Failed to decode JSON from the file '{file_path}'. Details: {e}")
        raise  # Re-raise the exception for further handling if needed
    except IOError as e:
        # Handle the case where there is an issue reading the file
        print(f"Error: An I/O error occurred while reading the file '{file_path}'. Details: {e}")
        raise  # Re-raise the exception for further handling if needed
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred while processing the file '{file_path}'. Details: {e}")
        raise  # Re-raise the exception for further handling if needed


# Saves data to a specified JSON file
def save_json(data, file_path):    
    try:
        # Try to open the file in write mode
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            try:
                # Try to save the data as JSON
                json.dump(data, f, ensure_ascii=False, indent=4)
                # print(f"Archivo guardado correctamente en {file_path}")
            except TypeError as e:
                # Error if data is not serializable to JSON
                print(f"Error al serializar los datos a JSON: {e}")
            except Exception as e:
                # Catch any other errors when saving data
                print(f"Error desconocido al guardar los datos en {file_path}: {e}")
    except PermissionError:
        # Error if you do not have permission to open or write the file
        print(f"Permiso denegado para escribir en el archivo: {file_path}")
    except FileNotFoundError:
        # Error if the file path does not exist
        print(f"El archivo o la ruta no existen: {file_path}")    
    except Exception as e:
        # Catch any other errors when opening the file
        print(f"Error al intentar abrir el archivo {file_path}: {e}")


# Validates that the data object has the expected structure and returns a boolean or an
# error messages
def validate_json_structure(data):    
    try:
        # Verify that the data object is a dictionary
        if not isinstance(data, dict):
            raise TypeError("El objeto data proporcionado no es un diccionario válido.")
        # Check that the 'intents' key exists and is not empty
        if ('intents' not in data or 
                not isinstance(data['intents'], list) or 
                len(data['intents']) == 0):
            raise ValueError("El archivo no contiene 'intents' o está vacío.")       
        # Validate each intent within 'intents'
        for intent in data['intents']:
            # Check that 'intent' is not None or empty
            if 'intent' not in intent or not intent['intent']:
                raise ValueError(f"La intención: '{intent['intent']}', no tiene un valor válido para 'intent'.")        
            # Check that 'examples' contains at least one non-empty, non-None example
            if ('examples' not in intent or 
                    not isinstance(intent['examples'], list) or 
                    len(intent['examples']) == 0):                    
                raise ValueError(
                                    f"La intención '{intent['intent']}' "
                                    f"no tiene ejemplos válidos ('examples')."
                                )
            if any(example is None or example.strip() == "" for example in intent['examples']):
                raise ValueError(
                                    f"Al menos un ejemplo de la intención '{intent['intent']}' "
                                    f"es inválido (None o vacío)."
                                )       
            # Check that 'response' is None or not empty
            if ('response' in intent and 
                    (intent['response'] is None or 
                    intent['response'].strip() == "")):
                raise ValueError(
                                    f"La intención '{intent['intent']}' tiene un 'response' "
                                    f"inválido (None o vacío)."
                                )
        # If all checks passed, the structure is valid
        return True
    except ValueError as e:
        print(f"Error de validación: {e}")
        return False
    except TypeError as e:
        print(f"Error de tipo: {e}")
        return False
    except KeyError as e:
        # In case of missing key errors
        print(f"Error de clave faltante: 'intents' o 'intent' no se encuentra en los datos: {e}")
        return False
    except Exception as e:
        # In case of any unexpected exception
        print(f"Error inesperado: {e}")
        return False


# Add intents from the new file to the base file without duplicating intents and adding
# only new examples.
def add_intents(intents_data, train_data):
    try:
        # Verify that intents_data and train_data are valid dictionaries
        if not isinstance(intents_data, dict) or not isinstance(train_data, dict):
            raise TypeError("Tanto intents_data como train_data deben ser diccionarios válidos.")
        # Verify that 'intents' key exists in both datasets
        if "intents" not in intents_data or "intents" not in train_data:
            raise KeyError("Falta la clave 'intents' en intents_data o train_data.")        
        # Iterate over each new intent in the 'new_data' file   
        for new_intent in train_data["intents"]:
            # Ensure each new intent is a dictionary
            if not isinstance(new_intent, dict):
                raise TypeError(
                                    f"Cada new_intent en train_data debe ser un dictionario, "
                                    f"pero se encontró: {type(new_intent)}"
                                )            
            # Find if the intent already exists in the base file
            existing_intent = next((intent 
                                    for intent in intents_data["intents"] 
                                    if intent["intent"] == new_intent["intent"]), None)
            if existing_intent:
                if "examples" not in new_intent:
                    raise KeyError(f"La clave 'examples' no existe en intent: {new_intent['intent']}")
                # If the intent already exists, add only the new examples (without duplicating examples)
                new_examples = [example 
                                for example in new_intent["examples"] 
                                if example not in existing_intent["examples"] and example.strip()]
                if new_examples:
                    existing_intent["examples"].extend(new_examples)
            else:
                # If the intention does not exist, add it completely
                intents_data["intents"].append(new_intent)
        return intents_data
    except TypeError as e:
        # Handle type errors (e.g., incorrect data types)
        print(f"Type error: {e}")
        return None
    except KeyError as e:
        # Handle missing key errors (e.g., missing 'intents' or 'examples')
        print(f"Key error: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")
        return None


# Move a file, receiving the source and destination, as well as renaming it.
def move_and_rename_file(source_file_path, new_name, destination_folder_path):
    try:
        # Create the subfolder if it does not exist
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)    
        # Get the full path to the destination file
        destination_file_path = os.path.join(destination_folder_path, new_name)
        # Check if the source file exists before attempting to move it
        if not os.path.isfile(source_file_path):
            raise FileNotFoundError(f"El archivo de origen {source_file_path} no se encontró.")
        # Move and rename the file to the specified destination
        os.rename(source_file_path, destination_file_path)         
        print(f"Archivo movido y renombrado a: {destination_file_path}")    
    except FileNotFoundError as e:
        # Handle file not found errors
        print(f"Error: {e}")
    except PermissionError:
        # Handle permission errors
        print(f"Error: No tienes permisos para mover o renombrar el archivo.")
    except OSError as e:
        # Handle general OS errors, such as invalid paths or disk issues
        print(f"Error de sistema operativo: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error inesperado al mover el archivo: {e}")