import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import time
from pynput import keyboard


class KeyTracker(threading.Thread):
    def __init__(self, key1, key2):
        threading.Thread.__init__(self)
        self.key1 = key1
        self.key2 = key2
        self.running = True
        self.pressed_keys = set()
        self.tap_counts = {key1: 0, key2: 0}

    def run(self):
        while self.running:
            if self.key1 in self.pressed_keys and self.key2 in self.pressed_keys:
                self.tap_counts[self.key1] += 1
                self.tap_counts[self.key2] += 1
            elif self.key1 in self.pressed_keys:
                self.tap_counts[self.key1] += 1
            elif self.key2 in self.pressed_keys:
                self.tap_counts[self.key2] += 1

            time.sleep(0.01)

    def stop(self):
        self.running = False


class App:
    def __init__(self, root):
        self.root = root
        self.key1 = 'a'
        self.key2 = 's'
        self.tracker = None

        root.title("JKPS")
        root.geometry("300x200")

        self.label1 = ttk.Label(root, text="Key 1: 0 taps/sec")
        self.label1.pack(pady=10)

        self.label2 = ttk.Label(root, text="Key 2: 0 taps/sec")
        self.label2.pack(pady=10)

    def on_press(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key)

        if key_name == self.key1 or key_name == self.key2:
            self.tracker.pressed_keys.add(key_name)

    def on_release(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key)

        if key_name == self.key1 or key_name == self.key2:
            self.tracker.pressed_keys.remove(key_name)

    def start_tracking(self):
        if not self.tracker:
            self.tracker = KeyTracker(self.key1, self.key2)
            self.tracker.start()
            self.root.bind('<KeyPress>', self.on_press)
            self.root.bind('<KeyRelease>', self.on_release)
            self.update_labels()

    def stop_tracking(self):
        if self.tracker:
            self.tracker.stop()
            self.tracker.join()
            self.tracker = None
            self.root.unbind('<KeyPress>')
            self.root.unbind('<KeyRelease>')
            self.label1.config(text=f"Key 1: 0 taps/sec")
            self.label2.config(text=f"Key 2: 0 taps/sec")

    def update_labels(self):
        if self.tracker:
            tap1 = self.tracker.tap_counts[self.key1]
            tap2 = self.tracker.tap_counts[self.key2]
            self.label1.config(text=f"Key 1: {tap1} taps/sec")
            self.label2.config(text=f"Key 2: {tap2} taps/sec")
            self.root.after(100, self.update_labels)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)

    start_button = ttk.Button(root, text="Start Tracking", command=app.start_tracking)
    start_button.pack(pady=10)

    stop_button = ttk.Button(root, text="Stop Tracking", command=app.stop_tracking)
    stop_button.pack(pady=10)

    root.mainloop()

   
