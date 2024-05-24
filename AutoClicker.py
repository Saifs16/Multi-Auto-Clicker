import customtkinter as ctk
import pyautogui
import threading
import numpy as np
from pynput import mouse
import keyboard
import time
import random
import logging
from tkinter import Toplevel, Label
import winsound

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.spots = []
        self.clicking = False
        self.setting_spots = False
        self.listener = None
        self.dot_windows = []

        self.click_count = 2  # Default number of clicks
        self.offset_range = 5  # Default offset range for random variation
        self.click_interval = 1  # Default delay between clicks
        self.set_interval = 2  # Default delay between sets of clicks

        self.setup_ui()
        keyboard.add_hotkey('ctrl+alt+q', self.emergency_stop)

    def setup_ui(self):
        self.root.title("Auto Clicker")
        self.root.geometry("500x400")

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # First row: Set Click Spots and Clear buttons
        self.btn_set_spots = ctk.CTkButton(frame, text="Set Click Spots", command=self.set_spots)
        self.btn_set_spots.grid(row=0, column=0, padx=10, pady=5)

        self.btn_clear_spots = ctk.CTkButton(frame, text="Clear", command=self.clear_spots, state=ctk.DISABLED)
        self.btn_clear_spots.grid(row=0, column=1, padx=10, pady=5)

        # Click spots label
        self.lbl_spots = ctk.CTkLabel(frame, text="Click Spots: Not set")
        self.lbl_spots.grid(row=1, column=0, columnspan=2, pady=5)

        # Text fields in a 2x2 grid
        self.lbl_click_count = ctk.CTkLabel(frame, text="Number of clicks per set:")
        self.lbl_click_count.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_click_count = ctk.CTkEntry(frame)
        self.entry_click_count.insert(0, "2")
        self.entry_click_count.grid(row=2, column=1, padx=5, pady=5)

        self.lbl_offset_range = ctk.CTkLabel(frame, text="Position variation (pixels):")
        self.lbl_offset_range.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_offset_range = ctk.CTkEntry(frame)
        self.entry_offset_range.insert(0, "5")
        self.entry_offset_range.grid(row=3, column=1, padx=5, pady=5)

        self.lbl_click_interval = ctk.CTkLabel(frame, text="Delay between clicks (seconds):")
        self.lbl_click_interval.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_click_interval = ctk.CTkEntry(frame)
        self.entry_click_interval.insert(0, "1")
        self.entry_click_interval.grid(row=4, column=1, padx=5, pady=5)

        self.lbl_set_interval = ctk.CTkLabel(frame, text="Delay between sets of clicks (seconds):")
        self.lbl_set_interval.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_set_interval = ctk.CTkEntry(frame)
        self.entry_set_interval.insert(0, "2")
        self.entry_set_interval.grid(row=5, column=1, padx=5, pady=5)

        # Start and Stop buttons in one row
        self.btn_start = ctk.CTkButton(frame, text="Start Clicking", command=self.start_clicking, state=ctk.DISABLED)
        self.btn_start.grid(row=6, column=0, padx=10, pady=10)

        self.btn_stop = ctk.CTkButton(frame, text="Stop Clicking", command=self.stop_clicking, state=ctk.DISABLED)
        self.btn_stop.grid(row=6, column=1, padx=10, pady=10)

        # Quit button underneath Start and Stop buttons on the right side
        btn_quit = ctk.CTkButton(frame, text="Quit", command=self.quit_program)
        btn_quit.grid(row=7, column=1, padx=10, pady=10, sticky="e")

    def on_click(self, x, y, button, pressed):
        if pressed and self.setting_spots:
            self.spots.append((x, y))
            self.create_dot(x, y)

            if len(self.spots) == self.click_count:
                self.setting_spots = False
                self.update_labels()
                self.listener.stop()
                self.btn_start.configure(state=ctk.NORMAL)
                self.btn_stop.configure(state=ctk.NORMAL)
                self.btn_clear_spots.configure(state=ctk.NORMAL)

    def set_spots(self):
        try:
            self.click_count = int(self.entry_click_count.get())
            self.offset_range = int(self.entry_offset_range.get())
            self.click_interval = float(self.entry_click_interval.get())
            self.set_interval = float(self.entry_set_interval.get())
        except ValueError:
            self.update_labels("Invalid input! Please enter valid numbers.")
            return

        self.clear_spots()
        self.spots = []
        self.setting_spots = True
        self.lbl_spots.configure(text=f"Click on {self.click_count} spots.")
        self.start_listener()

    def clear_spots(self):
        self.spots = []
        self.update_labels()
        self.btn_start.configure(state=ctk.DISABLED)
        self.btn_stop.configure(state=ctk.DISABLED)
        self.btn_clear_spots.configure(state=ctk.DISABLED)
        self.clear_dots()

    def start_listener(self):
        if self.listener is None or not self.listener.running:
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.start()

    def start_clicking(self):
        if self.clicking:
            return  # Prevent starting multiple threads

        self.clicking = True
        self.btn_start.configure(state=ctk.DISABLED)
        self.btn_stop.configure(state=ctk.NORMAL)
        self.btn_set_spots.configure(state=ctk.DISABLED)
        self.btn_clear_spots.configure(state=ctk.DISABLED)
        click_thread = threading.Thread(target=self.click_loop)
        click_thread.start()

    def stop_clicking(self):
        self.clicking = False

    def emergency_stop(self):
        self.stop_clicking()
        winsound.Beep(200, 150)  # Soft beep sound when stopping

    def click_loop(self):
        while self.clicking:
            for _ in range(self.click_count):
                if not self.clicking:
                    break
                for spot in self.spots:
                    if not self.clicking:
                        break
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
        self.btn_start.configure(state=ctk.NORMAL)
        self.btn_set_spots.configure(state=ctk.NORMAL)
        self.btn_clear_spots.configure(state=ctk.NORMAL)

    def update_labels(self, msg=None):
        if msg:
            self.lbl_spots.configure(text=msg)
        else:
            self.lbl_spots.configure(text=f"Click Spots: {self.spots if self.spots else 'Not set'}")

    def quit_program(self):
        self.stop_clicking()
        if self.listener is not None and self.listener.running:
            self.listener.stop()
        self.clear_dots()
        self.root.destroy()

    def create_dot(self, x, y):
        dot_window = Toplevel(self.root)
        dot_window.geometry(f"4x4+{x-5}+{y-5}")  # Center the dot
        dot_window.overrideredirect(1)
        dot_window.attributes("-topmost", True)
        dot_window.attributes("-alpha", 0.7)
        label = Label(dot_window, bg="red", width=1, height=1)
        label.pack(fill="both", expand=True)
        self.dot_windows.append(dot_window)

    def clear_dots(self):
        for window in self.dot_windows:
            window.destroy()
        self.dot_windows = []

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
    logging.basicConfig(level=logging.INFO)
    root = ctk.CTk()
    app = AutoClicker(root)
    root.mainloop()
