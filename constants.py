import os

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Define absolute paths within the project
DATA_PATH = os.path.join(PROJECT_ROOT, 'data')
MODELS_PATH = os.path.join(PROJECT_ROOT, 'models')
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
OLD_TRAIN_FILES_PATH = os.path.join(PROJECT_ROOT, 'data/old_training_files')
OLD_INTENTS_FILES_PATH = os.path.join(PROJECT_ROOT, 'data/old_intents_files')

# Paths to specific files
INTENTS_JSON_PATH = os.path.join(DATA_PATH, 'intents.json')
INTENTS_TRAIN_JSON_PATH = os.path.join(DATA_PATH, 'intents_train.json')

# Name of specific files
INTENTS_JSON = 'intents.json'
INTENTS_TRAIN_JSON = 'intents_train.json'
