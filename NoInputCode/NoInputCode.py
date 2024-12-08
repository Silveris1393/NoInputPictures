import os
import time
import tkinter as tk
from PIL import Image, ImageTk
from PIL import Image as PILImage 
from ctypes import Structure, windll, c_uint, sizeof, byref
import sys

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
    def __init__(self, image_folder, display_time=5):
        self.image_folder = image_folder
        self.display_time = display_time
        self.images = self.load_images(image_folder)
        if not self.images:
            print("No images found in folder:", image_folder)
            sys.exit(1)
        self.current_index = 0

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)  # Fullscreen mode
        self.root.configure(background='black')
        # Hide cursor if desired:
        self.root.config(cursor="none")

        # Bind keys or mouse movement to exit
        self.root.bind("<Escape>", self.exit_slideshow)
        self.root.bind("<Motion>", self.exit_slideshow)
        self.root.bind("<Key>", self.exit_slideshow)

        self.label = tk.Label(self.root, bg='black')
        self.label.pack(expand=True, fill='both')
        
        self.show_image()

    def load_images(self, folder):
        supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        files = [os.path.join(folder, f) for f in os.listdir(folder) 
                 if os.path.splitext(f)[1].lower() in supported_extensions]
        return files

    def show_image(self):
        image_path = self.images[self.current_index]
        img = Image.open(image_path)
        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(img)
        self.label.config(image=tk_image)
        self.label.image = tk_image  # Keep a reference

        self.current_index = (self.current_index + 1) % len(self.images)
        
        # Schedule next image
        self.root.after(self.display_time * 1000, self.show_image)

    def exit_slideshow(self, event=None):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# -----------------------
# Main Logic
# -----------------------
if __name__ == "__main__":
    # Set your desired folder of images
    IMAGE_FOLDER = r"C:\Users\User\Desktop\fotkes\fotiko fotkes\fotkes spausdinimui"
    
    # Idle threshold in seconds (5 minutes = 300 seconds)
    IDLE_THRESHOLD = 300  

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
