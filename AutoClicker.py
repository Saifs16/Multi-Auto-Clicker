import tkinter as tk
import pyautogui
import threading
import numpy as np
from pynput import mouse
import keyboard
import time
import random
import logging

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.spots = []
        self.clicking = False
        self.setting_spots = False
        self.listener = None

        self.click_count = 2  # Default number of clicks
        self.offset_range = 5  # Default offset range for random variation
        self.click_interval = 1  # Default delay between clicks
        self.set_interval = 2  # Default delay between sets of clicks

        self.setup_ui()
        keyboard.add_hotkey('ctrl+alt+q', self.stop_clicking)

    def setup_ui(self):
        self.root.title("Auto Clicker")
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        btn_set_spots = tk.Button(frame, text="Set Click Spots", command=self.set_spots)
        btn_set_spots.pack(side=tk.LEFT, padx=(0, 20))

        self.lbl_spots = tk.Label(self.root, text="Click Spots: Not set")
        self.lbl_spots.pack()

        self.lbl_click_count = tk.Label(self.root, text="Number of clicks per set:")
        self.lbl_click_count.pack()
        self.entry_click_count = tk.Entry(self.root)
        self.entry_click_count.insert(0, "2")
        self.entry_click_count.pack()

        self.lbl_offset_range = tk.Label(self.root, text="Position variation (pixels):")
        self.lbl_offset_range.pack()
        self.entry_offset_range = tk.Entry(self.root)
        self.entry_offset_range.insert(0, "5")
        self.entry_offset_range.pack()

        self.lbl_click_interval = tk.Label(self.root, text="Delay between clicks (seconds):")
        self.lbl_click_interval.pack()
        self.entry_click_interval = tk.Entry(self.root)
        self.entry_click_interval.insert(0, "1")
        self.entry_click_interval.pack()

        self.lbl_set_interval = tk.Label(self.root, text="Delay between sets of clicks (seconds):")
        self.lbl_set_interval.pack()
        self.entry_set_interval = tk.Entry(self.root)
        self.entry_set_interval.insert(0, "2")
        self.entry_set_interval.pack()

        self.btn_start = tk.Button(self.root, text="Start Clicking", command=self.start_clicking)
        self.btn_start.pack(pady=(20, 5))

        btn_stop = tk.Button(self.root, text="Stop Clicking", command=self.stop_clicking)
        btn_stop.pack()

        btn_quit = tk.Button(self.root, text="Quit", command=self.quit_program)
        btn_quit.pack(pady=(5, 20))

    def on_click(self, x, y, button, pressed):
        if pressed and self.setting_spots:
            self.spots.append((x, y))

            if len(self.spots) == self.click_count:
                self.setting_spots = False
                self.update_labels()
                self.listener.stop()

    def set_spots(self):
        try:
            self.click_count = int(self.entry_click_count.get())
            self.offset_range = int(self.entry_offset_range.get())
            self.click_interval = float(self.entry_click_interval.get())
            self.set_interval = float(self.entry_set_interval.get())
        except ValueError:
            self.update_labels("Invalid input! Please enter valid numbers.")
            return

        self.spots = []
        self.setting_spots = True
        self.lbl_spots.config(text=f"Click on {self.click_count} spots.")
        self.start_listener()

    def start_listener(self):
        if self.listener is None or not self.listener.running:
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.start()

    def start_clicking(self):
        if self.clicking:
            return  # Prevent starting multiple threads

        self.clicking = True
        self.btn_start.config(state=tk.DISABLED)
        click_thread = threading.Thread(target=self.click_loop)
        click_thread.start()

    def stop_clicking(self):
        self.clicking = False
        self.btn_start.config(state=tk.NORMAL)

    def click_loop(self):
        while self.clicking:
            for _ in range(self.click_count):
                for spot in self.spots:
                    offset_x = random.randint(-self.offset_range, self.offset_range)
                    offset_y = random.randint(-self.offset_range, self.offset_range)
                    random_spot = (spot[0] + offset_x, spot[1] + offset_y)

                    pyautogui.keyDown('shift')
                    pyautogui.click(random_spot)
                    pyautogui.keyUp('shift')

                    if not self.clicking:
                        break

                    time.sleep(self.click_interval)

                if not self.clicking:
                    break

                time.sleep(self.set_interval)

    def update_labels(self, msg=None):
        if msg:
            self.lbl_spots.config(text=msg)
        else:
            self.lbl_spots.config(text=f"Click Spots: {self.spots if self.spots else 'Not set'}")

    def quit_program(self):
        self.stop_clicking()
        if self.listener is not None and self.listener.running:
            self.listener.stop()
        self.root.destroy()

    def emergency_stop(self):
        self.stop_clicking()
        if self.listener is not None and self.listener.running:
            self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
