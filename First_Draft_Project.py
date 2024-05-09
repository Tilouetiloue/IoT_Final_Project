import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import *


# Creating Application Class
class Application(Frame) :

    # Constructor
    def __init__(self, master) :
        super(Application, self).__init__(master)
        # Pins
        self.DATA_Pin = 16
        self.CLK_Pin  = 20
        # Functions
        self.grid()
        self.setup()
        self.create_ui()
        self.checkdist()
        

        
        # Global Variables
        self.num_leds = 0
        self.max_leds = 10
        
        self.s_clk_flag = 0
        self.CmdMode  = 0x0000  # Work on 8-bit mode
        self.ON = 0x00ff  # 8-byte 1 data
        self.SHUT = 0x0000  # 8-byte 0 data
    # Setting up GPIO
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(24,GPIO.IN)
        GPIO.setup(19,GPIO.OUT)
        GPIO.setup(26,GPIO.OUT)
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(self.DATA_Pin, GPIO.OUT)
        GPIO.setup(self.CLK_Pin,  GPIO.OUT)

        GPIO.output(self.DATA_Pin, GPIO.LOW)
        GPIO.output(self.CLK_Pin,  GPIO.LOW)
        # Adding button events
        GPIO.add_event_detect(27, GPIO.FALLING, callback=self.button_callback_red, bouncetime=200)
        GPIO.add_event_detect(22, GPIO.FALLING, callback=self.button_callback_blue, bouncetime=200)
        
    
    # Creating Widgets
    def create_ui(self):
        # Text Field
        self.thresholdEntry = tk.Entry(self)
        # Save Button
        self.saveButton = tk.Button(self, text='Save Minimum', command=self.savethreshold)
        # Label
        self.thresholdLabel = tk.Label(self, text='Enter a threshold and press save: ')
        self.wasteIndicatorLabel = tk.Label(self, text='Current waste level')
        self.wasteLevelLabel = tk.Label(self, text='0%', bd=1, relief="solid", bg="white")
        # Positioning Widgets
        self.wasteIndicatorLabel.grid(row=0, column=0)
        self.wasteLevelLabel.grid(row=0, column=1)
        self.thresholdLabel.grid(row=1, column=0, sticky='w')
        self.thresholdEntry.grid(row=2, column=0, sticky='w')
        self.saveButton.grid(row=3, column=0, sticky='w')
    
    # Functions
    def checkdist(self):
        GPIO.output(23, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(23, GPIO.LOW)
        while not GPIO.input(24):
            pass
        t1 = time.time()
        while GPIO.input(24):
            pass
        t2 = time.time()
        waste_display = (t2-t1)*340/2
        self.wasteLevelLabel.config(text=str(waste_display))
        self.after(1000, self.checkdist)
    
    def button_callback_red(self, channel):
        GPIO.output(26, GPIO.HIGH)
        self.beep()
        
    def button_callback_blue(self, channel):
        GPIO.output(19, GPIO.HIGH)
        self.beep()
        
    def beep(self):
        GPIO.output(13, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(13, GPIO.LOW)
    
    def savethreshold(self):
        self.num_leds += 1
            
        if self.num_leds > self.max_leds:
            self.num_leds = 0
            
        LEDstate = (1 << self.num_leds) - 1

        # Send LED state to the LED bar and latch the data
        self.send16bitData(self.CmdMode)
        self.sendLED(LEDstate)
        self.latchData()
        time.sleep(0.1)
    
    def send16bitData(self, data):
        for i in range(0, 16):
            if data & 0x8000:
                GPIO.output(self.DATA_Pin, GPIO.HIGH)
            else:
                GPIO.output(self.DATA_Pin, GPIO.LOW)
            
            if self.s_clk_flag == True:
                GPIO.output(self.CLK_Pin, GPIO.LOW)
                self.s_clk_flag = 0
            else:
                GPIO.output(self.CLK_Pin, GPIO.HIGH)
                self.s_clk_flag = 1
            time.sleep(0.001)
            data = data << 1
    
    def sendLED(self, LEDstate):
        for i in range(0, 12):
            if (LEDstate & 0x0001) == True:
                self.send16bitData(self.ON)
            else:
                self.send16bitData(self.SHUT)
            LEDstate = LEDstate >> 1
    
    def latchData(self):
        latch_flag = 0
        GPIO.output(self.DATA_Pin, GPIO.LOW)
        
        time.sleep(0.05)
        for i in range(0, 8):
            if latch_flag == True:
                GPIO.output(self.DATA_Pin, GPIO.LOW)
                latch_flag = 0
            else:
                GPIO.output(self.DATA_Pin, GPIO.HIGH)
                latch_flag = 1
        time.sleep(0.05)
    
    def destroy(self, *args):
        GPIO.output(19, GPIO.LOW)
        GPIO.output(26, GPIO.LOW)
        GPIO.output(self.DATA_Pin, GPIO.LOW)
        GPIO.output(self.CLK_Pin,  GPIO.LOW)
        self.send16bitData(self.CmdMode)
        self.sendLED(0x0000)
        self.latchData()
        GPIO.cleanup()
        
# Running Application
root = tk.Tk()
root.title('GreenHouse Gas Sensor')
root.geometry('500x150')

app = Application(root)
app.mainloop()
