import tkinter as tk
import time
import keyboard

def write(text):
    for line in text:
        keyboard.write(line + '\n')
        time.sleep(1)
        keyboard.press_and_release('ctrl+tab')
        time.sleep(1)

def get_multiline_text():
    def on_send():
        global entered_text
        entered_text = text_entry.get("1.0", tk.END).strip()
        root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("Multiline Text Entry")

    # Create a text entry widget
    text_entry = tk.Text(root, wrap=tk.WORD, width=40, height=10)
    text_entry.pack(pady=10)

    # Create a "Send" button
    send_button = tk.Button(root, text="Send", command=on_send)
    send_button.pack()

    # Run the Tkinter event loop
    root.mainloop()

    return entered_text  # Return the entered text after the window is closed

if __name__ == "__main__":
    text = get_multiline_text()
    input("Appuyez sur Entrée pour commencer")
    time.sleep(5)
    write(text.split("\n"))