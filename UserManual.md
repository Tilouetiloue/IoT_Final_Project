# Waste Management User Manual

### How to use the waste management system

Presets: 
- When the script is run the system is automatically on and the waste bin is locked.
- The code to lock and unlock the bin is "Red, Blue, Red, Blue"
- Default bin size is 5 meters
- Default threshold is 99%

How to:
- Step 1: Run script
- Step 2: Change bin size to the size of your waste bin by entering the size in meters, do so inside the text box labeled with "Enter bin size:"
- Step 3: Set the desired threshold to consider the bin full, by entering a number to represent the desired threshold inside the text box labeled with "Enter a threshold and press save:"
- Step 4: Watch the gui waste level percentage to get the percentage of waste inside your bin

To Access Bin:
Simply enter the correct button sequence, The red LED will then close and the green LED will open, this indicates that access to the bin is authorized and no warnings will occur if the lid is lifted off of the bin.
##### IMPORTANT:
DO NOT press buttons on case of incorrect codes. #4 of ERROR Cases will cover more on this, however it is important to know that doing so will only cause confusion to the user and their code inputs as the application will still register button clicks even while the buzzer is sounding.

### ERROR Cases
1. Unauthorized access
    This problem will make a warning window open indicating that the bin has been lifted without authorized access or while locked.
    fix: To fix the error if the bin was opened by trusted personelle while locked, simply enter the code to unlock while the warning window is opened and preceed with tasks.

2. Threshold being exceeded:
    This will cause the "Warning:" label to indicate that the full threshold has been reached and the bin must be emptied.

3. Incorrect code sequence
    This error occurs when the button sequence to access the bin is incorrect. In this case a warning window will open after a buzzer sounds for 1 second, that indicates that the button sequence was incorrect. DO NOT press buttons while buzzer is sounding as this will register the input bringing possible confusion with inputs.
    fix: if inputs were pressed while buzzer was sounding, a simple fix is to get the code wrong, stop pressing buttons and preceed after closing the window, to enter the correct code.

4. Invalid Inputs
    This error occurs when user does not input valid inputs for threshold or bin size. It is important to note that these fields only take number inputs. If letters are present, the input will be rejected, no changes will be made and a warning window will pop-up indicating incorrect inputs.
    Ex. Inputting 50 for threshold will set the percentage threshold to 50%, inputting 30 in bin size will make bin size equal to 30 meters