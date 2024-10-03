# menjalankan PIN GPIO
import RPi.GPIO as GPIO
from time import sleep, time
import threading
 
# menjalankan tflite
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import time
import matplotlib.pyplot as plt

from PIL import Image
import time

import tkinter as tk
from tkinter import Label

 # menjalankan Picamera2
from picamera2 import Picamera2
from libcamera import controls
from gpiozero import AngularServo
from time import sleep


# RUNNING CAMERA MODULE V3
picam2 = Picamera2()
picam2.preview_configuration.main.size = (720, 720)
picam2.configure("preview")
picam2.start(show_preview=True)

label1 = 'kuning_campuran'
label2 = 'hijau_muda'
label3 = 'biru_muda'

import csv
import os


#class_names = ['kuning_campuran', 'hijau_muda', 'biru_muda', 'tidak_dikenali']

class_names = ['putih','hijautua', 'hitam', 'merah', 'orange', 'putih_campuran','kuning', 'kuning_campuran'
               , 'hijaumuda', 'birulangit', 'birutua', 'coklat','emas']

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
    success = picam2.autofocus_cycle()
    job = picam2.autofocus_cycle(wait=False)
    success = picam2.wait(job)

    name_file = "output_tflite.jpg"

    if(success):
        picam2.capture_file(name_file)
        Image.open(name_file).resize((224, 224))
        #deteksi_tutup_botol()
        # Path to the .tflite model
        #model_path = "model_raspberypi/model_b.tflite"
        model_path = "model_a_epoch_100_1080.tflite"

        # Load the TFLite model
        interpreter = tflite.Interpreter(model_path=model_path)

        # Allocate tensors
        interpreter.allocate_tensors()

        # Get input and output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        #image_path = "output.jpg"
        #image = Image.open(image_path).resize((224, 224))
        
        input_image_path = 'output_tflite.jpg'
        output_image_path = 'output_compress_tf.jpg'

        image = Image.open(resize_image(input_image_path, output_image_path)).resize((224, 224))
        

        # Convert image to numpy array and add batch dimension
        input_data = np.expand_dims(np.array(image, dtype=np.float32), axis=0)

        # Normalize the image if required by your model (e.g., scale pixel values to [0, 1])
        input_data = input_data / 255.0

        # Set the input tensor
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # Record start time
        start_time = time.time()

        # Run inference
        interpreter.invoke()

        # Record end time
        end_time = time.time()

        # Calculate prediction time
        prediction_time = np.round(end_time - start_time, 3) * 1000

        # Get the output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])

        predicted_class = np.argmax(output_data, axis=1)

        # If you have class labels, you can map them back
        #class_file = 'class6.txt'
        #with open(class_file, 'r') as f:
            #class_names = f.read().splitlines()

        # Create a dictionary of class indices based on the class.txt file
        class_indices = {idx: class_name for idx, class_name in enumerate(class_names)}

        # Map predicted class to label
        predicted_label = class_indices[predicted_class[0]]

        # Get predicted probability
        predicted_probability = output_data[0][predicted_class[0]]

        # Convert probability to percentage
        predicted_probability_percentage = np.round(predicted_probability * 100, 2)

        # Create a list with label, prediction time, and accuracy
        result_data = [predicted_label, f"{prediction_time:.0f}", f"{predicted_probability_percentage}"]

        # Path to the CSV file
        csv_file_path = "classification_results_1_0_1080_1.csv"
        
        # Write the results to the CSV file
        write_to_csv(csv_file_path, result_data)
    

        print(f"{predicted_label}")
        print(f"{prediction_time:.4f}")
        print(f"{predicted_probability_percentage:.2f}")
        
        #picam2.stop()
        #return "berhasil ambil gambar"
    #else:
        #return "gagal ambil gambar"
        #picam2.stop()
    #picam2.stop()
        
        
def write_to_csv(file_path, data):
    file_exists = os.path.isfile(file_path)
    
    # Open the CSV file in append mode
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header only if the file doesn't already exist
        if not file_exists:
            writer.writerow(["Label", "Prediction Time (s)", "Accuracy (%)"])
        
        # Write the data (label, prediction_time, accuracy)
        writer.writerow(data)
    
#function deteksi tutup botol model   
def deteksi_tutup_botol():
        
    # Path to the .tflite model
    model_path = "tf_lite_mode_xception.tflite"

    # Load the TFLite model
    interpreter = tflite.Interpreter(model_path=model_path)

    # Allocate tensors
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


    #image_path = "output.jpg"
    #image = Image.open(image_path).resize((224, 224))
    
    input_image_path = 'output_tflite.jpg'
    output_image_path = 'output_compress_tf.jpg'

    image = Image.open(resize_image(input_image_path, output_image_path)).resize((224, 224))
    
    

    # Convert image to numpy array and add batch dimension
    input_data = np.expand_dims(np.array(image, dtype=np.float32), axis=0)

    # Normalize the image if required by your model (e.g., scale pixel values to [0, 1])
    input_data = input_data / 255.0

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Record start time
    start_time = time.time()

    # Run inference
    interpreter.invoke()

    # Record end time
    end_time = time.time()

    # Calculate prediction time
    prediction_time = end_time - start_time

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    predicted_class = np.argmax(output_data, axis=1)

    # If you have class labels, you can map them back
    class_file = 'class5.txt'
    with open(class_file, 'r') as f:
        class_names = f.read().splitlines()

    # Create a dictionary of class indices based on the class.txt file
    class_indices = {idx: class_name for idx, class_name in enumerate(class_names)}

    # Map predicted class to label
    predicted_label = class_indices[predicted_class[0]]

    # Get predicted probability
    predicted_probability = output_data[0][predicted_class[0]]

    # Convert probability to percentage
    predicted_probability_percentage = predicted_probability * 100
    
    print(f"{predicted_label}")
    print(f"{prediction_time:.4f}")
    print(f"{predicted_probability_percentage:.2f}")
    
    #return (
       # f"{predicted_label}",
        #f"{prediction_time:.4f}",
       # f"{predicted_probability_percentage:.2f}"
       # )


window = tk.Tk()
window.title("APPS CAPTURE CAMERA")
btn_capture = tk.Button(window, text = "Capture", command=capture_sample)
btn_capture.pack()



window.mainloop()
