import wikipedia
import cv2 as cv
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query)
        return summary
    except wikipedia.exceptions.DisambiguationError:
        return "The query is ambiguous. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find information on that topic."
def process_image(file_path):
    img = cv.imread(file_path)
    if img is None:
        return "Error loading image."
    blank = np.zeros(img.shape[:2], dtype='uint8')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, thresh_image = cv.threshold(gray, 160, 255, cv.THRESH_BINARY)
    sides = cv.Canny(thresh_image, 50, 175)
    contours, _ = cv.findContours(sides, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    shape = "Unknown"
    for i, contour in enumerate(contours):
        if i == 0:
            continue
        end_correction = 0.01 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, end_correction, True)
        if len(approx) == 3:
            shape = 'Triangle'
        elif len(approx) == 4:
            shape = 'Quadrilateral'
        elif len(approx) == 5:
            shape = 'Pentagon'
        elif len(approx) == 6:
            shape = 'Hexagon'
        elif len(approx) == 7:
            shape = 'Heptagon'
        elif len(approx) == 8:
            shape = 'Octagon'
        elif len(approx) == 9:
            shape = 'Nonagon'
        else:
            shape='Circle'
    return f"Detected Shape: {shape}"
def display_image(file_path):
    try:
        img = Image.open(file_path)
        img.show()  
    except IOError:
        messagebox.showerror("Error", "Error loading image.")
def display_message(title, message):
    print(f"{title}\n{'-'*len(title)}")
    print(message)
    print()
def main():
    root = tk.Tk()
    root.withdraw()  
    display_message("Welcome!", "Hello! I am Qt. Ask me anything, or upload an image for shape detection.\nType 'upload image' for shape detection.\nType 'exit' to end the chat.")
    print('''                             ╱|、
                          (˚ˎ 。7  
                           |、˜〵          
                          じしˍ,)ノ

'''
)
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'upload image':
            file_path = filedialog.askopenfilename(
                title="Select a JPG File",
                filetypes=[("JPG Files", "*.jpg")]
            )
            if file_path:
                display_image(file_path)
                shape_info = process_image(file_path)
                display_message("Image Processing Result", shape_info)
            else:
                display_message("No File Selected", "No file selected. Please try again.")
        else:
            wiki_summary = get_wikipedia_summary(user_input)
            display_message("Wikipedia Summary", wiki_summary)
if __name__ == "__main__":
    main()
