import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import *
import tkinter.font as tkfont
from tkinter import messagebox
# Creating Application Class
class Application(Frame) :

    # Constructor
    def __init__(self, master) :
        super(Application, self).__init__(master)
        # Pins
        self.DATA_Pin = 16
        self.CLK_Pin  = 20
        self.SENSOR_OUT = 23
        self.SENSOR_IN = 24
        self.GREEN_LED = 19
        self.RED_LED = 26
        self.RED_BUTTON = 27
        self.BLUE_BUTTON = 22
        self.BUZZER = 13
        # Global Variables
        self.num_leds = 0
        self.max_leds = 10
        
        self.password = "1010"
        self.input_password = ""
        self.passwd_clicks = 0
        
        self.is_locked = True
        
        self.entry_bin_size = tk.StringVar()
        self.bin_size = 5
        self.entry_threshold = tk.StringVar()
        self.threshold = 99
        
        self.s_clk_flag = 0
        self.CmdMode  = 0x0000  # Work on 8-bit mode
        self.ON = 0x00ff  # 8-byte 1 data
        self.SHUT = 0x0000  # 8-byte 0 data
        
        # Functions
        self.grid()
        self.create_ui()
        self.setup()
        self.process()
        
    # Setting up GPIO
    def setup(self):
        # Setmode and warnings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # Setting up pins
        GPIO.setup(self.SENSOR_OUT,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.SENSOR_IN,GPIO.IN)
        GPIO.setup(self.GREEN_LED,GPIO.OUT)
        GPIO.setup(self.RED_LED,GPIO.OUT)
        GPIO.setup(self.RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUZZER, GPIO.OUT)
        GPIO.setup(self.DATA_Pin, GPIO.OUT)
        GPIO.setup(self.CLK_Pin,  GPIO.OUT)
        # Setting default outputs
        GPIO.output(self.DATA_Pin, GPIO.LOW)
        GPIO.output(self.CLK_Pin,  GPIO.LOW)
        GPIO.output(26,GPIO.HIGH)
        # Adding button events
        GPIO.add_event_detect(27, GPIO.FALLING, callback=self.button_callback_red, bouncetime=200)
        GPIO.add_event_detect(22, GPIO.FALLING, callback=self.button_callback_blue, bouncetime=200)
        
    
    # Creating Widgets
    def create_ui(self):
        # Fonts
        bold_font = tkfont.Font(family='Helvetica', size=12, weight='bold')
        # Text Fields
        self.thresholdEntry = tk.Entry(self, textvariable=self.entry_threshold)
        self.sizeEntry = tk.Entry(self, textvariable=self.entry_bin_size)
        # Save Buttons
        self.saveThreshButton = tk.Button(self, text='Save Threshold', command=self.savethreshold)
        self.saveSizeButton = tk.Button(self, text='Save Size', command=self.savesize)
        # Labels
        self.sizeLabel = tk.Label(self, text='Enter bin size: ')
        self.thresholdLabel = tk.Label(self, text='Enter a threshold and press save: ')
        self.wasteIndicatorLabel = tk.Label(self, text='Current waste level: ')
        self.wasteLevelLabel = tk.Label(self, text='0%', bd=1, relief='solid', bg='white', font=bold_font, padx=5, pady=5)
        self.warningLabel = tk.Label(self, text='Warning: ', font=bold_font, padx=10, pady=10)
        # Positioning Widgets
        self.wasteIndicatorLabel.grid(row=0, column=0)
        self.wasteLevelLabel.grid(row=0, column=1)
        self.thresholdLabel.grid(row=1, column=0, sticky='w')
        self.thresholdEntry.grid(row=2, column=0, sticky='w')
        self.saveThreshButton.grid(row=3, column=0, sticky='w')
        self.sizeLabel.grid(row=1, column=3, sticky='w')
        self.sizeEntry.grid(row=2, column=3, sticky='w')
        self.saveSizeButton.grid(row=3, column=3, sticky='w')
        self.warningLabel.grid(row=4, column=0, sticky='w')
    
    # Functions

    # Process that runs every second
    def process(self):
        self.checkdist()
        self.checkthreshold()
        self.after(1000, self.process)
    
    # Function to check distance of waste and authorized access
    def checkdist(self):
        # Emit ultrasonic sound
        GPIO.output(23, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(23, GPIO.LOW)
        while not GPIO.input(24):
            pass
        t1 = time.time()
        while GPIO.input(24):
            pass
        t2 = time.time()
        # Calculating distance
        distance = (t2-t1)*340/2
        print(distance)
        # Check if the bin has authorized access or not
        if(self.is_locked and distance > self.bin_size):
            self.buzz(2)
            self.warning("Unauthorized access to waste bin")
        elif(self.is_locked and distance <= self.bin_size):
            waste = self.bin_size - distance
            percentage = (waste/self.bin_size) * 100
            self.checkleds(percentage)
    
    # Red Button callback function to enter password
    def button_callback_red(self, channel):
        self.beep()
        # Add inputs to password
        if not (self.passwd_clicks == len(self.password)):
            self.passwd_clicks += 1
            self.input_password += str(1)
        else:
            # Check if passwords match
            if(self.input_password == self.password):
                self.input_password = ""
                self.passwd_clicks = 0
                # Lock or Unlock
                if(self.is_locked):
                    self.is_locked = False
                    GPIO.output(26, GPIO.LOW)
                    GPIO.output(19, GPIO.HIGH)
                else:
                    self.is_locked = True
                    GPIO.output(26, GPIO.HIGH)
                    GPIO.output(19, GPIO.LOW)
            else:
                # Incorrect sequence
                self.buzz(1)
                self.input_password = ""
                self.passwd_clicks = 0
                self.warning("Wrong button sequence")

    # Blue Button callback function to enter password
    def button_callback_blue(self, channel):
        self.beep()
        # Add inputs to password
        if not (self.passwd_clicks == len(self.password)):
            self.passwd_clicks += 1
            self.input_password += str(0)
        else:
            # Check if passwords match
            if(self.input_password == self.password):
                self.input_password = ""
                self.passwd_clicks = 0
                # Lock or Unlock
                if(self.is_locked):
                    self.is_locked = False
                    GPIO.output(26, GPIO.LOW)
                    GPIO.output(19, GPIO.HIGH)
                else:
                    self.is_locked = True
                    GPIO.output(26, GPIO.HIGH)
                    GPIO.output(19, GPIO.LOW)
            else:
                # Incorrect sequence
                self.buzz(1)
                self.input_password = ""
                self.passwd_clicks = 0
                self.warning("Wrong button sequence")
    
    # Function that beeps the buzzer
    def beep(self):
        GPIO.output(13, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(13, GPIO.LOW)
    
    # Function that sounds the buzzer for given time
    def buzz(self, duration):
        GPIO.output(13, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(13, GPIO.LOW)
    
    # Function to open warning window
    def warning(self, message):
        messagebox.showwarning("Warning", message)
    
    # Function to open bar LED, LEDs based on percentage
    def checkleds(self, percentage):
        # Default LED state
        LEDstate = 0b0000000000
        # Checking which state is needed
        if(10 < percentage < 20):
            LEDstate = 0b1
        elif(20 < percentage < 30):
            LEDstate = 0b11
        elif(30 < percentage < 40):
            LEDstate = 0b111
        elif(40 < percentage < 50):
            LEDstate = 0b1111
        elif(50 < percentage < 60):
            LEDstate = 0b11111
        elif(60 < percentage < 70):
            LEDstate = 0b111111
        elif(70 < percentage < 80):
            LEDstate = 0b1111111
        elif(80 < percentage < 90):
            LEDstate = 0b11111111
        elif(90 < percentage < 100):
            LEDstate = 0b111111111
        elif(percentage >= 100):
            LEDstate = 0b1111111111
        
        # Setting visual indicators
        self.setledbar(LEDstate)
        self.setwastelabel(percentage)
    
    # Function to check level of waste depending on threshold, warning when needed
    def checkthreshold(self):
        current_percentage = float(self.wasteLevelLabel["text"].rstrip("%"))
        if (current_percentage >= self.threshold):
            self.warningLabel.config(text="Warning: Waste level is passed full threshold")
        else:
            self.warningLabel.config(text="Warning: ")
    
    # Function to save Threshold
    def savethreshold(self):
        try:
            set_threshold = float(self.entry_threshold.get())
            
            self.threshold = set_threshold
        except:
            self.warning("Invalid Input, need a number")
    
    # Function to send data to LED bar
    def setledbar(self, LEDstate):
        self.send16bitData(self.CmdMode)
        self.sendLED(LEDstate)
        self.latchData()
    
    # Function to set the waste level label
    def setwastelabel(self, percentage):
        waste_level = "{:.1%}".format(percentage / 100)
        self.wasteLevelLabel.config(text=waste_level)
    
    # Function to save bin size
    def savesize(self):
        try:
            set_size = float(self.entry_bin_size.get())
            
            self.bin_size = set_size
        except:
            self.warning("Invalid Input, need a number")
    
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