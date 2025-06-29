import tkinter as tk
from tkinter import ttk

class MenuPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.build_menu()

    def build_menu(self):
        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)
        ttk.Label(container, text="PixelMasterX", font=("Segoe UI", 20, "bold")).pack(pady=(0, 30))
        ttk.Button(container, text="File Conversion", style="Accent.TButton",
                   command=self.controller.show_conversion_frame).pack(fill="x", pady=10)
        ttk.Button(container, text="Image Editor", style="Accent.TButton",
                   command=self.controller.show_image_editor_frame).pack(fill="x", pady=10)
        ttk.Button(container, text="Remove Background", style="Accent.TButton",
                   command=self.controller.show_remove_background).pack(fill="x", pady=10)

