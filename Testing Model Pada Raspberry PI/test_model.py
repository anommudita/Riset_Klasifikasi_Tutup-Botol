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
 
 # menjalankan Picamera2
from picamera2 import Picamera2
from libcamera import controls
from gpiozero import AngularServo
from time import sleep

import csv
import os

#servo1
servo = AngularServo(10, min_pulse_width=0.0006, max_pulse_width=0.0023)
#servo2
servo2 = AngularServo(21, min_pulse_width=0.0006, max_pulse_width=0.0023)
#servo3
servo3 = AngularServo(16, min_pulse_width=0.0006, max_pulse_width=0.0023) 
 
# PIN Motor Stepper
DIR_PIN = 27   # Direction pin
STEP_PIN = 22  # Step/Pulse pin
ENA_PIN = 17    # Enable pin

# PIN Sensor Infrared
# IR MAIN
SENSOR_PIN = 11
#IR1
SENSOR_PIN2 = 9
#IR2
SENSOR_PIN3 = 20
#IR3
SENSOR_PIN4 = 12

#IR UNKNON
SENSOR_PIN5 = 26
 
 
# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup GPIO pins
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENA_PIN, GPIO.OUT)

# IR
GPIO.setup(SENSOR_PIN, GPIO.IN)


# RUNNING CAMERA MODULE V3
picam2 = Picamera2()
picam2.preview_configuration.main.size = (720, 720)
#picam2.configure("preview")
#picam2.start(show_preview=True)
picam2.start()
# Angle Servo First Time Machine Sorting AUTOBCS
servo.angle = -2
servo2.angle = -2
servo3.angle = -2


#kelas label
"""
putih
putihcampuran
kuning
kuningcampuran
hijaumuda
birulangit
birutua
coklat
emas
hijautua
hitam
merah
orange
"""

"""
putih
hijautua
hitam
merah
orange
putihcampuran
kuning
kuningcampuran
hijaumuda
birulangit
birutua
coklat
emas

"""


label1 = 'kuning'
label2 = 'kuning_campuran'
label3 = 'orange'


class_names = ['putih','hijautua', 'hitam', 'merah', 'orange', 'putih_campuran','kuning', 'kuning_campuran'
               , 'hijaumuda', 'birulangit', 'birutua', 'coklat','emas']



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

    name_file = "output.jpg"

    if(success):
        picam2.capture_file(name_file)
        Image.open(name_file).resize((224, 224))

    
#function deteksi tutup botol mobileNETV2    
def deteksi_tutup_botol():
        
    # Path to the .tflite model
    # mobileneV2_epoch_100_1.4.tflite
    # mobileneV2_epoch_100.tflite
    model_path = "xception.tflite"

    # Load the TFLite model
    interpreter = tflite.Interpreter(model_path=model_path)

    # Allocate tensors
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    input_image_path = 'output.jpg'
    output_image_path = 'output_compress.jpg'

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
    csv_file_path = "xception_test.csv"
    
    # Write the results to the CSV file
    write_to_csv(csv_file_path, result_data)
    
    return (
        f"{predicted_label}",
        f"{prediction_time}",
        f"{predicted_probability_percentage}"
        )
def step_motor(direction, delay):
    
    print('step motor')
    GPIO.output(DIR_PIN, direction) # motor stepper mengarah mundur jika LOW
    GPIO.output(ENA_PIN, GPIO.LOW)  # Enable the motor
    
    
    while True:
        
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:  # Sensor  IR UTAMA detected an object
            print("Object detected. Stopping motor...")
            servo.angle = -2
            servo2.angle = -2
            servo3.angle = -2

            GPIO.output(ENA_PIN, GPIO.HIGH)  # Disable the motor
            
            #ambil gambar
            capture_sample()
            
            #hasil deteksi gambar
            result = deteksi_tutup_botol()
            
            #kelas atau label
            kelas = result[0]
            #hasil akurasinya
            akurasi = float(result[2])
    
            print(result)
            
            s1 = 0
            
            # ketika sesuai dengan label dan akurasi diatas 60%  # slot penampung 1
            if((kelas == label1)):
                servo.angle = -80
                s1+1
                print(s1)

                
                #gaser motor sedetik agar perulangan bisa berjalan
                go_motor(GPIO.LOW, 0.00001)
            elif((kelas == label2) ): # slot penampung 2
                servo2.angle = -80
                
                #gaser motor sedetik agar perulangan bisa berjalan
                go_motor(GPIO.LOW, 0.00001)
                
            elif((kelas == label3)): # slot penampung 3
                servo3.angle = -80
                
                #gaser motor sedetik agar perulangan bisa berjalan
                go_motor(GPIO.LOW, 0.00001)
              
            # menuju slot tidak dikenali
            else:    
                go_motor(GPIO.LOW, 0.00001)

        
        # These two lines result in 1 step
        GPIO.output(STEP_PIN, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        sleep(delay)
        
        
def go_motor(direction, delay):
    
    GPIO.output(DIR_PIN, direction)
    GPIO.output(ENA_PIN, GPIO.LOW)
    
    
    print('go motor')
    # Catat waktu mulai
    start_time = time.time()

    # Durasi maksimum untuk loop dalam detik
    max_duration = 1

    while time.time() - start_time < max_duration:
        GPIO.output(STEP_PIN, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        sleep(delay)


    motorHandler()

        
        
 
def motorHandler():
    
    """
    Handler function to control motor operations.
    """                    
    step_motor(GPIO.LOW, 0.00001)
    
   
 
def motorStop():
    """
    Function to stop the motor and clean up GPIO settings.
    """
    print("Stopping motor...")
    GPIO.output(STEP_PIN, GPIO.LOW)  # Ensure motor is stopped
    GPIO.output(ENA_PIN, GPIO.LOW)  # Disable the motor
    GPIO.cleanup()  # Clean up GPIO settings
 
if __name__ == "__main__":
        motorHandler()
