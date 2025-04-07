''' 
To resolve the issue of not finding the /src folder when importing functions, change the current 
working directory of the Python process to the root directory of the project.
'''
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
from src.chatbot import process_message

# Create a column to display errors
error_column = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True, visible=False)

def main(page: ft.Page):
    try:
        # Window settings
        page.window.width = 400             # window's width is 400 px
        page.window.height = 600            # window's height is 600 px
        page.window.resizable = False       # window is not resizable
        page.window.maximizable = False     # window is not maximizable
        page.window.center()                # window is aligned in the center of the screen    
        # Create a container to display the conversation history
        # auto_scroll=True performs automatic scrolling, if scroll_to is used it must be false
        conversation_history = ft.Column(scroll=ft.ScrollMode.ADAPTIVE,
                                            auto_scroll=False, 
                                            expand=True,
                                        )
        # Add initial text to the page""
        conversation_history.controls.append(ft.TextField("¡Hola! Soy un chatbot. "
                                                            "\n¿Cómo puedo ayudarte?",
                                                            multiline=True, 
                                                            border=ft.InputBorder.NONE)
                                            )
        page.add(conversation_history)    
        # Variable to track whether the conversation has ended
        conversation_ended = False

        # Function that is executed when the user sends the message
        def on_submit(e):
            # Reference a variable that is in the scope of a parent function (but not 
            # in global scope).
            nonlocal conversation_ended
            try:
                # If the conversation has already ended, do not process any more entries
                if conversation_ended:
                    return        
                # Remove spaces at the beginning and end
                user_input = input_field.value.strip()
                # If the user types 'exit' or 'Exit', we end the conversation
                if user_input.lower() == 'exit':
                    conversation_history.controls.append(ft.TextField("Gracias por conversar. "
                                                                        "¡Hasta luego!",
                                                                        multiline=True, 
                                                                        border=ft.InputBorder.NONE)
                                                        )
                    # Scroll down to the bottom to always keep the newest messages visible
                    conversation_history.scroll_to(offset=-1, duration=1)
                    # Disable the text field and mark the conversation as over
                    input_field.disabled = True
                    conversation_ended = True
                    # Refresh page to reflect disabled status
                    page.update() 
                    return  # End the conversation        
                # Add user input to history (right-aligned and multi-line)
                conversation_history.controls.append(
                    ft.Row(
                        [ft.TextField(f"Tú: \n{user_input}",
                                        text_align= ft.TextAlign.RIGHT,
                                        multiline=True, 
                                        border=ft.InputBorder.NONE)
                        ],
                        # Aligns to the right when using wrap, otherwise 'alignment'
                        run_alignment=ft.MainAxisAlignment.END,
                        #the Row will put child controls into additional rows (runs) if they don't 
                        # fit a single row.            
                        wrap=True
                    )
                )
                # The response is obtained based on the message entered by the user
                response = process_message(user_input)         
                # Add the chatbot's response to the history (left-aligned and multi-line)
                conversation_history.controls.append(
                    ft.Row(
                        [ft.TextField(f"Chatbot: \n{response}",
                                        multiline=True, 
                                        border=ft.InputBorder.NONE)
                        ],
                        # Aligns to the left when using wrap, otherwise 'alignment'
                        run_alignment=ft.MainAxisAlignment.START,
                        #the Row will put child controls into additional rows (runs) if they don't 
                        # fit a single row.
                        wrap=True, 
                    )
                )        
                # Refresh the page to reflect the full history
                page.update()
                # Scroll down to the bottom to always keep the newest messages visible
                conversation_history.scroll_to(offset=-1, duration=1)
                # Clear the text field for the next interaction
                input_field.value = ""
                input_field.focus()
            except Exception as e:
                    print(f"Error in the on_submit function: {e}")
                    error_column.controls.append(ft.TextField(f"Error al procesar tu mensaje: \n{e}", 
                                                                multiline=True, 
                                                                border=ft.InputBorder.UNDERLINE)
                                                )
                    error_column.visible=True
                    page.update()
                    # Scroll down to the bottom to always keep the newest messages visible
                    conversation_history.scroll_to(offset=-1, duration=1)
                    # Scroll down to the bottom to always keep the newest error visible
                    error_column.scroll_to(offset=-1, duration=1)
                    input_field.value = ""
                    input_field.focus()

        # Create a text field to enter messages
        input_field = ft.TextField(label="Escribe tu mensaje", on_submit=on_submit)
        page.add(input_field)
        # Focus on the text field after adding it to the page
        input_field.focus()
        # Add the error column to the page to display errors
        page.add(error_column)
    except Exception as e:
        print(f"Error in main function: {e}")
        error_column.controls.append(ft.TextField(f"Hubo un error en la aplicación: {e}", 
                                                    multiline=True, 
                                                    border=ft.InputBorder.UNDERLINE)
                                    )
        error_column.visible=True
        page.update()
        # Scroll down to the bottom to always keep the newest messages visible
        conversation_history.scroll_to(offset=-1, duration=1)
        # Scroll down to the bottom to always keep the newest error visible
        error_column.scroll_to(offset=-1, duration=1)
        input_field.value = ""
        input_field.focus()        


# Run the Flet application
ft.app(target=main)
