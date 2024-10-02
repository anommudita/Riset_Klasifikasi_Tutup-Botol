import tkinter
import customtkinter
from PIL import Image, ImageTk  # Import Pillow for image handling
import subprocess

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.is_sorting = False
        self.process = None

        # configure window
        self.title("Application AutoBCS")
        self.geometry(f"{1000}x{760}")

        # configure grid layout (4x3)
        self.grid_columnconfigure(1, weight=2)  # Image section (middle)
        self.grid_columnconfigure(2, weight=3)  # Conveyor section (right side)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        # Title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Bottle Caps Sorting", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Choose Sorting 1
        self.choose_klasifikasi_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="Selector 1:")
        self.choose_klasifikasi_label1.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.choose_klasifikasi1 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Choose...", "Putih", "Putih Campuran", 
            "Kuning", "Kuning Campuran", "Hijau Muda", "Hijau Tua", "Biru Muda", "Biru Tua", "Coklat", "Emas", "Hitam", "Merah", "Jingga"], 
            command=self.change_appearance_mode_event)
        self.choose_klasifikasi1.grid(row=2, column=0, padx=20, pady=(10, 10))

        # Choose Sorting 2
        self.choose_klasifikasi_label2 = customtkinter.CTkLabel(self.sidebar_frame, text="Selector 2:")
        self.choose_klasifikasi_label2.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.choose_klasifikasi2 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Choose...", "Putih", "Putih Campuran", 
            "Kuning", "Kuning Campuran", "Hijau Muda", "Hijau Tua", "Biru Muda", "Biru Tua", "Coklat", "Emas", "Hitam", "Merah", "Jingga"], 
            command=self.change_appearance_mode_event)
        self.choose_klasifikasi2.grid(row=4, column=0, padx=20, pady=(10, 10))

        # Choose Sorting 3
        self.choose_klasifikasi_label3 = customtkinter.CTkLabel(self.sidebar_frame, text="Selector 3:")
        self.choose_klasifikasi_label3.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.choose_klasifikasi3 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Choose...", "Putih", "Putih Campuran", 
            "Kuning", "Kuning Campuran", "Hijau Muda", "Hijau Tua", "Biru Muda", "Biru Tua", "Coklat", "Emas", "Hitam", "Merah", "Jingga"], 
            command=self.change_appearance_mode_event)
        self.choose_klasifikasi3.grid(row=6, column=0, padx=20, pady=(10, 10))

        # RUN/STOP Button
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Run", fg_color="green", hover_color="darkgreen", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=7, column=0, padx=20, pady=30)


        # Load and display static image
        self.image_frame = customtkinter.CTkFrame(self, width=500, corner_radius=10)
        self.image_frame.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=20, pady=20)

        self.load_static_image("dashboard1.png")  # Provide the correct path to the image file

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def sidebar_button_event(self):
        if not self.is_sorting:
            self.is_sorting = True
            sorting_option1 = self.choose_klasifikasi1.get()
            sorting_option2 = self.choose_klasifikasi2.get()
            sorting_option3 = self.choose_klasifikasi3.get()
            self.print_label(sorting_option1, sorting_option2, sorting_option3)
            self.run_sorting_process()

            self.sidebar_button_2.configure(text="Stop", fg_color="red", hover_color="darkred")
        else:
            self.is_sorting = False
            self.stop_sorting_process()

            self.sidebar_button_2.configure(text="Run", fg_color="green", hover_color="darkgreen")

    def run_sorting_process(self):
        try:
            sorting_option1 = self.choose_klasifikasi1.get()
            sorting_option2 = self.choose_klasifikasi2.get()
            sorting_option3 = self.choose_klasifikasi3.get()
            self.process = subprocess.Popen(["python", "machine.py", sorting_option1, sorting_option2, sorting_option3])
        except Exception as e:
            print(f"Error starting IoT process: {e}")
        
    def stop_sorting_process(self):
        if self.process:
             # Pass a "stop" command to the IoT program to handle the stop logic
            subprocess.Popen(["python", "machine.py", "stop"])
            self.process.terminate()
            self.process = None
            print("Sorting process stopped.")

    def print_label(self, option1, option2, option3):
        print(f"Sorting Option 1: {option1}")
        print(f"Sorting Option 2: {option2}")
        print(f"Sorting Option 3: {option3}")

    def load_static_image(self, image_path):
        try:
            # Load image using PIL
            img = Image.open(image_path)
            img = img.resize((720, 720))  # Resize image if needed
            self.photo = ImageTk.PhotoImage(img)

            # Create label to display the image
            self.image_label = customtkinter.CTkLabel(self.image_frame, image=self.photo, text="")
            self.image_label.grid(row=0, column=0, padx=10, pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
