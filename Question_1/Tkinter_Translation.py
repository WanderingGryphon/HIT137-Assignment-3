import tkinter as tk
from tkinter import ttk
from googletrans import Translator

# A decorator for logging actions
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"Action: {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

# Base class for GUI (Encapsulation of GUI-related elements)
class BaseGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CAS 137 App")
        self.geometry("400x400")

        # Labels and text areas
        self.label_input = tk.Label(self, text="Enter Text:")
        self.label_input.pack(pady=6)

        self.text_input = tk.Text(self, height=5, width=40)
        self.text_input.pack()

        self.label_output = tk.Label(self, text="Translated Text:")
        self.label_output.pack(pady=6)

        self.text_output = tk.Text(self, height=5, width=40)
        self.text_output.pack()

        # Encapsulating source and target language dropdown menus
        self.label_source = tk.Label(self, text="Source Language")
        self.label_source.pack(pady=6)

        # Set the foreground color of the combobox text to black as text was hiding behind the white color
        style = ttk.Style()
        style.configure('TCombobox', foreground='black')

        # List of  Translate supported languages 
        self.languages = {"English": "en", "French": "fr", "German": "de", "Spanish": "es", "Italian": "it", "Nepali": "ne", "Vietnamese": "vi", "Bengali": "bn"}

        self.source_language = ttk.Combobox(self, values=list(self.languages.keys()), style='TCombobox')
        self.source_language.pack()
        self.source_language.current(0)  # Default: English

        self.label_target = tk.Label(self, text="Target Language")
        self.label_target.pack(pady=6) #pady for vertical padding

        self.target_language = ttk.Combobox(self, values=list(self.languages.keys()), style='TCombobox')
        self.target_language.pack()
        self.target_language.current(5)  # Default: Nepali

        # Translate button
        self.button_translate = tk.Button(self, text="Translate", command=self.translate_text)
        self.button_translate.pack(pady=15)

    @log_action
    def show_translation(self, translation):
        self.text_output.delete(1.0, tk.END)  # Clear previous translation
        self.text_output.insert(tk.END, translation)  # Show new translation

# Class for handling translation using Google Translate (Encapsulation of translation logic)
class TranslationModel:
    def __init__(self):
        self.translator = Translator()  # Initialize the Google Translate API

    @log_action
    def translate(self, source_text, src_lang, tgt_lang):
        # Translate text using Google Translate
        translation = self.translator.translate(source_text, src=self.languages[src_lang], dest=self.languages[tgt_lang])
        return translation.text

# Derived class using Multiple Inheritance (BaseGUI and TranslationModel)
class TranslationApp(BaseGUI, TranslationModel):
    def __init__(self):
        # Initializing both parent classes
        BaseGUI.__init__(self)
        TranslationModel.__init__(self)

    @log_action
    def translate_text(self):
        source_text = self.text_input.get("1.0", tk.END).strip()  # Get input text
        src_lang = self.source_language.get()  # Get source language
        tgt_lang = self.target_language.get()  # Get target language

        # Perform the translation using the Google Translate API
        translation = self.translate(source_text, src_lang, tgt_lang)
        self.show_translation(translation)  # Display the translation

# Instantiate and run the application
if __name__ == "__main__":
    app = TranslationApp()
    app.mainloop()
