 # menjalankan Picamera2
from picamera2 import Picamera2
from libcamera import controls
picam2 = Picamera2()
picam2.preview_configuration.main.size = (720, 720)
picam2.configure("preview")
picam2.start(show_preview=True)
from PIL import Image
import time

import tkinter as tk
from tkinter import Label

counter = 0

# function resize gambar
def resize_image(input_path, output_path, size=(224, 224)):
    """
    Resize image to the specified size and save it to output_path.
    """
    with Image.open(input_path) as img:
        # Resize image
        resized_img = img.resize(size, Image.ANTIALIAS)
        # Save resized image
        resized_img.save(output_path)
        return output_path


# function ambil gambar secara autofocus
def capture_sample():
    
    global counter
    
    #fokus
    success = picam2.autofocus_cycle()
    job = picam2.autofocus_cycle(wait=False)
    success = picam2.wait(job)

    name_file = "output_720_1.jpg"

    if(success):
        picam2.capture_file(name_file)
        Image.open(name_file).resize((224, 224))
        
        input_image_path = name_file
    
        counter+=1
        name_capture = f"hijautua{counter}.jpg"
    
        print(name_capture)
        
        # buat folder hijautua 
        output_image_path = f"hijautua/{name_capture}"

        image = Image.open(resize_image(input_image_path, output_image_path)).resize((224, 224))
        
    
window = tk.Tk()
window.title("APPS CAPTURE CAMERA")
btn_capture = tk.Button(window, text = "Capture", command=capture_sample)
btn_capture.pack()



window.mainloop()




   