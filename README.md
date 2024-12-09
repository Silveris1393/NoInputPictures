Idle Picture Show

Overview

This Python application creates a fullscreen slideshow from images stored in a specified folder. It displays the images one by one, loading them in manageable chunks to handle large collections efficiently. The application prevents image repetition within each cycle and handles EXIF orientation to ensure vertical photos are displayed correctly. Mainly was made for people who uses TV as a monitor and wants to show pictures when being idle. 

Features

Chunk-Based Loading:

Processes images in chunks (default: 20 images) to efficiently handle large collections.

Loads the next chunk after finishing the current one.

Prevents Repetition:

Keeps track of shown images to avoid repetition until all images are displayed.

EXIF Orientation Support:

Corrects image orientation using EXIF data to ensure vertical photos are displayed properly.

Fullscreen Slideshow:

Runs in fullscreen mode with a hidden cursor for distraction-free viewing.

Randomized Order:

Randomizes the order of image display for variety.

Idle-Based Activation:

Starts the slideshow after a specified idle time (default: 10 seconds).

Supports Large Image Collections:

Efficiently manages memory to support collections of any size.

Requirements

Python 3.7 or higher

Required Python libraries:

Pillow

tkinter

Installation

Clone or download the repository containing this script.

Ensure Python and the required libraries are installed.

pip install pillow

Place your images in the desired folder.

Usage

Set the folder path containing your images:

IMAGE_FOLDER = r"C:\your\destination"

(Optional) Adjust the idle time threshold:

IDLE_THRESHOLD = 10  # Idle time in seconds

Run the script:

python slideshow.py

Exit the slideshow by pressing Escape or any key.

Customization

Chunk Size

Change the chunk_size parameter to adjust how many images are preloaded at a time:

slideshow = SlideshowApp(IMAGE_FOLDER, display_time=5, chunk_size=20)

Display Time

Modify the display_time parameter to adjust how long each image is displayed:

slideshow = SlideshowApp(IMAGE_FOLDER, display_time=5)

Handling Orientation

The application automatically corrects orientation using EXIF data.
If this behavior is not desired, you can comment out the following line in the code:

img = ImageOps.exif_transpose(img)

Known Limitations

Performance on Low-End Machines:

Preloading large images may still cause slight delays on older or slower machines.

No Support for Non-JPEG Formats:

Currently, only .jpg and .jpeg images are supported. To support other formats, update the supported_extensions list.

Contributing

Feel free to fork the repository and make improvements. Submit a pull request for review and inclusion.

License

This project is licensed under the MIT License. See the LICENSE file for details.
