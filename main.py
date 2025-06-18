import os
import sys
import tkinter as tk

from GUI import GUI
from Limiter import Controller

root = tk.Tk()

if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "favicon.ico")
else:
    icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
root.iconbitmap(icon_path)

gui = GUI(root)
controller = Controller()
gui.set_controller(controller)
controller.set_gui(gui)


def save_window_geometry():
    with open("window_geometry.txt", "w") as f:
        f.write(root.geometry())


def load_window_geometry():
    if os.path.exists("window_geometry.txt"):
        with open("window_geometry.txt", "r") as f:
            geometry = f.read().strip()
            if geometry:
                root.geometry(geometry)


def main():
    root.title("Ultimate File Converter")
    load_window_geometry()
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def on_close():
    save_window_geometry()
    root.destroy()


if __name__ == "__main__":
    main()

