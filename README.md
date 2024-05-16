# Multi-Auto-Clicker
A customizable auto-clicker designed for specific use cases where multiple click spots are needed. This tool allows you to automate clicking at multiple locations on your screen with configurable intervals and position variations.

## Features
-Set multiple click spots.
-Configure the number of clicks per set.
-Adjustable delay between individual clicks.
-Adjustable delay between sets of clicks.
-Randomized position variation for each click to simulate more human-like interaction.
-Stop clicking via a keyboard shortcut(left control + left alt + Q).


## Requirements
-Python 3.x


-pyautogui library


-pynput library


-numpy library


-keyboard library


-tkinter library (comes with Python)



## Installation
Clone the repository or download the source code.
Install the required libraries:
```bash
pip install pyautogui pynput numpy keyboard
```

## Usage
Run the multi_auto_clicker.py script:
```bash
python multi_auto_clicker.py
```

The GUI will appear, allowing you to configure the auto-clicker settings.
### Configuration Options
**Set Click Spots: Click this button to start setting the click spots. Click on the desired locations on your screen. The number of clicks to be set is defined by the "Number of clicks per set" field.**


**Number of clicks per set: Enter the number of clicks you want per set.**


**Position variation (pixels): Enter the maximum pixel offset for click variations.**


**Delay between clicks (seconds): Enter the delay between individual clicks.**


**Delay between sets of clicks (seconds): Enter the delay between sets of clicks.**


## Starting and Stopping


-Start Clicking: Begins the auto-clicking process.
-Stop Clicking: Stops the auto-clicking process.
-Quit: Closes the application.


## Stop Auto-Clicker


-Press Ctrl+Alt+Q at any time to stop the auto-clicking process.


## Shortcomings and future improvements


-**Sound/Click Feedback**: Lack of audio feedback for each click action.

-**User Interface**: Enhance the UI to be more visually appealing and user-friendly.


-**Customize Keybind**: Allow user to pick the keybind to stop auto-clicker.

-**Disable Buttons**: Disable and Enable Buttons when approperiate. 

-**Always On Top**: Allowed user to have the auto-clicker be ontop of other programs. 
