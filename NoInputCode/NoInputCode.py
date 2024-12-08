import os
import time
import tkinter as tk
from PIL import Image, ImageTk
from ctypes import Structure, windll, c_uint, sizeof, byref
import sys
import pyautogui
import random

# -----------------------
# Idle Time Detection (Windows)
# -----------------------
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_time():
    # Returns idle time in seconds
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

# -----------------------
# Slideshow Functionality
# -----------------------
class SlideshowApp:
    def __init__(self, root_folder, display_time=5):
        self.root_folder = root_folder
        self.display_time = display_time
        self.images = self.load_images(root_folder)
        if not self.images:
            print("No JPEG images found in folder or subfolders:", root_folder)
            sys.exit(1)
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)  # Fullscreen mode
        self.root.configure(background='black')
        self.root.config(cursor="none")  # Hide cursor

        # Bind keys or mouse movement to exit
        self.root.bind("<Escape>", self.exit_slideshow)
       # self.root.bind("<Motion>", self.exit_slideshow)
        self.root.bind("<Key>", self.exit_slideshow)

        self.label = tk.Label(self.root, bg='black')
        self.label.pack(expand=True, fill='both')

        self.show_random_image()

    def load_images(self, folder):
        supported_extensions = ['.jpg', '.jpeg']
        images = []
        # Walk through the root folder and subfolders
        for root, _, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1].lower() in supported_extensions:
                    images.append(os.path.join(root, file))
        return images

    def show_random_image(self):
        image_path = random.choice(self.images)  # Pick a random image
        img = Image.open(image_path)

        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        orig_width, orig_height = img.size

        # Calculate a scale factor that fits the image inside the screen while keeping aspect ratio
        scale_factor = min(screen_width / orig_width, screen_height / orig_height)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(img)
        self.label.config(image=tk_image)
        self.label.image = tk_image  # Keep a reference
        pyautogui.move(40, 0)  # Move mouse 1 pixel to the right
        pyautogui.move(-1, 0)  # Move mouse 1 pixel back to the left
        # Schedule next random image
        self.root.after(self.display_time * 1000, self.show_random_image)


#     def show_image(self):
#         image_path = self.images[self.current_index]
#         img = Image.open(image_path)
#         # Get screen size
#         screen_width = self.root.winfo_screenwidth()
#         screen_height = self.root.winfo_screenheight()
#        # img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
#         orig_width, orig_height = img.size

# # Calculate a scale factor that fits the image inside the screen while keeping aspect ratio
#         scale_factor = min(screen_width / orig_width, screen_height / orig_height)

#         new_width = int(orig_width * scale_factor)
#         new_height = int(orig_height * scale_factor)

#         img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
#         tk_image = ImageTk.PhotoImage(img)
#         self.label.config(image=tk_image)
#         self.label.image = tk_image  # Keep a reference

#         self.current_index = (self.current_index + 1) % len(self.images)
#         # Simulate mouse movement to prevent sleep
   

#         # Schedule next image
#         self.root.after(self.display_time * 1000, self.show_image)
#         pyautogui.move(1, 0)  # Move mouse 1 pixel to the right
#         pyautogui.move(-1, 0)  # Move mouse 1 pixel back to the left


    def exit_slideshow(self, event=None):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
    
       
 
# -----------------------
# Main Logic
# -----------------------
if __name__ == "__main__":
    # Set your desired folder of images
    IMAGE_FOLDER = r"C:\Users\User\Desktop\fotkes\fotiko fotkes"
    
    # Idle threshold in seconds (5 minutes = 300 seconds)
    IDLE_THRESHOLD = 10  

    print("Monitoring idle time. Will start slideshow after 5 minutes of no activity.")
    while True:
        idle = get_idle_time()
        if idle >= IDLE_THRESHOLD:
            # Start the slideshow
            slideshow = SlideshowApp(IMAGE_FOLDER, display_time=5)
            slideshow.run()
            # After slideshow exits, reset idle monitoring
            print("Slideshow exited. Monitoring again.")
        time.sleep(5)  # Check every 5 seconds to reduce CPU usage.
