''' To solve the problem of not finding the /src folder when import functions.'''
import os
import sys
# Get the root directory of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Changes the current working directory of the Python process to the project root directory.
os.chdir(project_root)
# Check if the root directory is not already in sys.path
if project_root not in sys.path:
    sys.path.append(project_root)   # Add the root directory to sys.path



import flet as ft
from src.chatbot import train_classifier, retrain_classifier
from src.data_preprocessing import load_data

def main(page: ft.Page):
    # Window settings
    page.window.width = 400             # window's width is 400 px
    page.window.height = 600            # window's height is 600 px
    page.window.resizable = False       # window is not resizable
    page.window.maximizable = False     # window is not maximizable
    page.window.center()                # window is aligned in the center of the screen
    
    
    # Paso 1: Ejecutar chatbot.py para entrenar el modelo y obtener el clasificador
    classifier = train_classifier()

    # Crear un contenedor para mostrar el historial de la conversación
    # auto_scroll= True realiza el scroll automatico, si se usa scroll_to debe ser false
    conversation_history = ft.Column(scroll=ft.ScrollMode.ADAPTIVE,
                                        auto_scroll=False, 
                                        expand=True,
                                    )
    

    # Agregar texto inicial en la página
    conversation_history.controls.append(ft.Text("¡Hola! Soy un chatbot. \n¿Cómo puedo ayudarte?"))
    page.add(conversation_history)

    # Variable para rastrear si la conversación ha terminado
    conversation_ended = False
    
    
    # Función que se ejecuta cuando el usuario envía el mensaje
    def on_submit(e):
        nonlocal conversation_ended

        # Si la conversación ya terminó, no procesar más entradas
        if conversation_ended:
            return
        
        
        user_input = input_field.value.strip()  # Elimina espacios al principio y final

        # Si el usuario escribe 'exit', finalizamos la conversación
        if user_input.lower() == 'exit':
            conversation_history.controls.append(ft.Text("Gracias por conversar. ¡Hasta luego!"))
            page.update()
            
            # Deshabilitar el campo de texto y marcar la conversación como terminada
            input_field.disabled = True
            conversation_ended = True
            page.update()  # Para reflejar el estado deshabilitado
            return  # Finaliza la conversación

        # Agregar la entrada del usuario al historial (alineado a la derecha)
        conversation_history.controls.append(
            ft.Row(
                [ft.Text(f"Tú: {user_input}")],
                wrap=True,
                alignment=ft.MainAxisAlignment.END # Alinea a la derecha
            )
        )

        # Clasificar la intención del mensaje del usuario
        intent = classifier.predict(user_input)

        # Responder con la intención y la respuesta
        for intent_data in classifier.model.named_steps['multinomialnb'].classes_:
            if intent == intent_data:
                response = next(item['response'] for item in load_data('data/intents.json')['intents'] if item['intent'] == intent_data)
                break
            
        # Agregar la respuesta del chatbot al historial (alineado a la izquierda)
        conversation_history.controls.append(
            ft.Row(
                #[ft.Text(f"Chatbot, tú intensión es: {intent}")],
                [ft.Text(f"Chatbot: {response}")],
                wrap=True,
                alignment=ft.MainAxisAlignment.START  # Alinea a la izquierda
            )
        )
        
        # Actualizar la página para reflejar el historial completo
        page.update()
        # se realiza el scroll al final para asi dejar siempre visible los mensajes mas nuevos
        conversation_history.scroll_to(offset=-1, duration=1)
        # Limpiar el campo de texto para la próxima interacción
        input_field.value = ""
        input_field.focus()

    # Crear un campo de texto para ingresar mensajes
    input_field = ft.TextField(label="Escribe tu mensaje", on_submit=on_submit)
    page.add(input_field)
    # Inicializar el foco en el campo de texto después de agregarlo a la página
    input_field.focus()
    

# Ejecutar la aplicación Flet
ft.app(target=main)
