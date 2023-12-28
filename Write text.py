import time
import keyboard
import tkinter as tk

def get_multiline_text():
    def on_send():
        global entered_text
        entered_text = text_entry.get("1.0", tk.END).strip()
        root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("Entrez les descriptions")

    # Create a main frame with padding
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack()

    # Create a label
    label = tk.Label(main_frame, text="Entrez les descriptions")
    label.pack()

    # Create a text entry widget
    text_entry = tk.Text(main_frame, wrap=tk.WORD, width=40, height=10)
    text_entry.pack(pady=10)

    # Create a "Send" button
    send_button = tk.Button(main_frame, text="Envoyer", command=on_send)
    send_button.pack()

    # Run the Tkinter event loop
    root.mainloop()

    return entered_text  # Return the entered text after the window is closed

def write(description):
    # Récupérer le texte saisi par l'utilisateur
    text_to_type = "#laugh #hilariouspetstiktoktv #smilesquad😝 #PetHumor #adorable #bell #funnyfriends #therealquirkyone #joyful #wildliferehab #grin"

    # Écrire le texte avec le clavier
    keyboard.write(description + '\n')
    time.sleep(2)
    words = text_to_type.split()
    for word in words:
        keyboard.write(word)
        time.sleep(1.5+len(word)*0.02)  # Délai supplémentaire après chaque mot (ajustez si nécessaire)
        keyboard.press_and_release('enter')

if __name__ == "__main__":
    descriptions = get_multiline_text().split("\n")
    input("Appuyez sur Entrée pour commencer")
    time.sleep(5)
    for description in descriptions:
        write(description)
        keyboard.press_and_release('ctrl+tab')
        time.sleep(1)
    keyboard.press_and_release('ctrl+shift+tab')