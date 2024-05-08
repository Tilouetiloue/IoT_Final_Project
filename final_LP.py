import tkinter as tk
from tkinter import *


# Creating Application Class
class Application(Frame) :

    # Constructor
    def __init__(self, master) :
        super(Application, self).__init__(master)
        self.grid()
        self.setup()
        self.createWidget()

        
    # Setting up GPIO
    def setup(self):
        pass
    
    # Creating Widgets
    def createWidget(self):
        # Text Field
        self.thresholdEntry = tk.Entry(self)
        # Save Button
        self.saveButton = tk.Button(self, text='Save Minimum')
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

# Running Application
root = tk.Tk()
root.title('GreenHouse Gas Sensor')
root.geometry('500x150')

app = Application(root)
app.mainloop()

