import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

# This class sets up the basic window
class BasicWindow:
    def __init__(self, root):
        # Creates a window with a title and size
        self.root = root
        self.root.title("AI Image Classifier")
        self.root.geometry("600x400")

# This class handles opening image files
class FileOperations:
    def open_file(self):
        # Opens a file dialog for selecting an image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        if file_path:
            # Loads and resizes the selected image
            img = Image.open(file_path)
            img.thumbnail((200, 200))
            img = ImageTk.PhotoImage(img)
            self.img_label.config(image=img)
            self.img_label.image = img
            # Classifies the selected image
            self.classify_image(file_path)

# This class combines both window setup and file operations
class App(BasicWindow, FileOperations):
    def __init__(self, root):
        # Initializes the window and image display
        super().__init__(root)
        self.img_label = tk.Label(root)
        self.img_label.pack(pady=20)
        
        # Button to open image files
        self.open_btn = tk.Button(root, text="Open Image", command=self.open_file)
        self.open_btn.pack(pady=10)
        
        # Label to display classification result
        self.result_label = tk.Label(root, text="Classification Result: ", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

    # This function logs when an image is classified
    def log_decorator(func):
        def wrapper(self, *args, **kwargs):
            print(f"Classifying image: {args[0]}")  # Prints the file path of the image
            return func(self, *args, **kwargs)  # Calls the original function
        return wrapper
    
    # Classifies the image and updates the label with the result
    @log_decorator
    def classify_image(self, file_path):
        result = self._simple_image_classifier(file_path)
        self.result_label.config(text=f"Classification Result: {result}")
    
    # This function randomly classifies the image (as a simple mockup)
    def _simple_image_classifier(self, file_path):
        classes = ["Dog", "Cat", "Bird", "Car"]
        return random.choice(classes)  # Chooses a random class

# Starts the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
