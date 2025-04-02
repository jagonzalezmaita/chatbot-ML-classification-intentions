import os

# Obtener la ruta absoluta al directorio raíz del proyecto
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Definir rutas absoluta dentro del proyecto
DATA_PATH = os.path.join(PROJECT_ROOT, 'data')
MODELS_PATH = os.path.join(PROJECT_ROOT, 'models')
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')

# Rutas a archivos específicos
INTENTS_JSON_PATH = os.path.join(DATA_PATH, 'intents.json')
INTENTS_TRAIN_JSON_PATH = os.path.join(DATA_PATH, 'intents_train.json')

# print(PROJECT_ROOT)
# print(DATA_PATH)
# print(MODELS_PATH)
# print(SRC_PATH)
# print(INTENTS_JSON_PATH)