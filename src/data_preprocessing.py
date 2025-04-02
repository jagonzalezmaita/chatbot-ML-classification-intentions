import json

# Load a JSON file and return dictionary with data from a JSON file.
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