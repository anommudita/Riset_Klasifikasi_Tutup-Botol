import sys
from time import sleep

if sys.argv[1] == "default":
    sleep(0.1)
    from rpi_lcd import LCD
    lcd = LCD()
    lcd.text("AutoBCS Telah Aktif",1, "center")
    lcd.text("sedang menyortir....",2, "center")
    lcd.text(f"S1=0  S2=0", 3, "center")
    lcd.text(f"S3=0  S4=0", 4, "center")
else:
    sleep(0.1)
    from rpi_lcd import LCD
    lcd = LCD()
    lcd.clear()
     # Read the counter values passed from the subprocess
    label_lcd = sys.argv[1]
    time_execute = sys.argv[2]
    percentage_accuracy = sys.argv[3]
    counter1 = sys.argv[4]
    counter2 = sys.argv[5]
    counter3 = sys.argv[6]
    counter4 = sys.argv[7]

    lcd.text(f"{label_lcd}", 1, "center")
    lcd.text(f"{time_execute}ms | {percentage_accuracy}%", 2, "center")
    lcd.text(f"S1={counter1}  S2={counter2}", 3, "center")
    lcd.text(f"S3={counter3}  S4={counter4}", 4, "center")
    
