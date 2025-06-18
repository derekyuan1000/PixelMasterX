import tkinter as tk
from tkinter import ttk, Menu
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import Conversions as info
import threading
import Menu

class GUI:
    def __init__(self, ROOT) -> None:
        self.ROOT = ROOT
        self.ROOT.title("PixelMasterX")
        self.ROOT.geometry("800x700")
        self.ROOT.resizable(True, True)

        # Apply dark theme
        self.style = tb.Style(theme="darkly")
        self.ROOT.configure(bg=self.style.colors.bg)

        # --- Main Frame ---
        self.MAIN_FRAME = ttk.Frame(self.ROOT, padding=15)
        self.MAIN_FRAME.pack(fill="both", expand=True)

        # --- Menu Page (Home) ---
        self.menu_page = Menu.MenuPage(self.MAIN_FRAME, self)
        self.menu_page.pack(fill="both", expand=True)

        # --- Header ---
        header_frame = ttk.Frame(self.MAIN_FRAME)
        header_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(header_frame, text="PIXELMASTERX",
                  font=("Segoe UI", 16, "bold")).pack(side="left")

        # --- Conversion Frame ---
        self.conversion_frame = ttk.Frame(self.MAIN_FRAME)
        self.build_conversion_ui(self.conversion_frame)

        # --- Remove Background Frame ---
        self.remove_bg_frame = ttk.Frame(self.MAIN_FRAME)
        self.build_remove_bg_ui(self.remove_bg_frame)

        # --- About Frame ---
        self.about_frame = ttk.Frame(self.MAIN_FRAME)
        self.build_about_ui(self.about_frame)

        self.ROOT.bind("<F11>", self.toggle_fullscreen)
        self.ROOT.bind("<Escape>", self.exit_fullscreen)
        self.fullscreen = False

    def show_menu_page(self):
        self.conversion_frame.pack_forget()
        self.remove_bg_frame.pack_forget()
        self.about_frame.pack_forget()
        self.menu_page.pack(fill="both", expand=True)

    def show_conversion_frame(self):
        self.menu_page.pack_forget()
        self.about_frame.pack_forget()
        self.remove_bg_frame.pack_forget()
        self.conversion_frame.pack(fill="both", expand=True)

    def show_remove_background(self):
        self.menu_page.pack_forget()
        self.conversion_frame.pack_forget()
        self.about_frame.pack_forget()
        self.remove_bg_frame.pack(fill="both", expand=True)

    def show_about(self):
        self.menu_page.pack_forget()
        self.conversion_frame.pack_forget()
        self.remove_bg_frame.pack_forget()
        self.about_frame.pack(fill="both", expand=True)

    def build_about_ui(self, parent):
        about_container = ttk.Frame(parent, padding=20)
        about_container.pack(fill="both", expand=True)

        ttk.Label(about_container, text="About PixelMasterX",
                  font=("Segoe UI", 14, "bold")).pack(anchor="center", pady=(0, 20))

        ttk.Label(about_container, text="A modern, easy-to-use file conversion and image editing utility.",
                  font=("Segoe UI", 11)).pack(anchor="center", pady=5)

        ttk.Label(about_container, text="Supports conversion between various image, audio, and video formats.",
                  font=("Segoe UI", 11)).pack(anchor="center", pady=5)

        ttk.Label(about_container, text="© 2025 Derek Yuan",
                  font=("Segoe UI", 10)).pack(anchor="center", pady=(30, 5))

        ttk.Label(about_container, text="MIT License",
                  font=("Segoe UI", 10)).pack(anchor="center", pady=5)

    def build_conversion_ui(self, parent):
        # Tab control for different conversion types
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Single File Conversion Tab ---
        single_frame = ttk.Frame(notebook, padding=15)
        notebook.add(single_frame, text="Single File")

        # Title with icon-like prefix
        ttk.Label(single_frame, text="» Single File Conversion",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # Short description
        ttk.Label(single_frame, text="Convert individual files between different formats.",
                 font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 10))

        # File selection frame
        file_frame = ttk.LabelFrame(single_frame, text="Source File", padding=15)
        file_frame.pack(fill="x", pady=(0, 15))

        file_row = ttk.Frame(file_frame)
        file_row.pack(fill="x", pady=5)
        self.chosen_files = tk.StringVar(value="")
        self.file_paths = []
        ttk.Entry(file_row, textvariable=self.chosen_files, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(file_row, text="Browse Files", style="Accent.TButton",
                   command=lambda: self.controller.update_chosen_files()).pack(side="right")

        # Conversion options frame
        options_frame = ttk.LabelFrame(single_frame, text="Conversion Options", padding=15)
        options_frame.pack(fill="x", pady=(0, 15))

        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill="x", pady=5)

        from_frame = ttk.Frame(format_frame)
        from_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(from_frame, text="From Format:").pack(anchor="w", pady=(0, 5))
        self.SINGLE_FORMAT_FROM_BOX = ttk.Combobox(from_frame, values=info.file_formats, state="readonly")
        self.SINGLE_FORMAT_FROM_BOX.pack(fill="x")
        self.SINGLE_FORMAT_FROM_BOX.bind('<<ComboboxSelected>>', lambda x: self.controller.update_to_format())

        to_frame = ttk.Frame(format_frame)
        to_frame.pack(side="right", fill="x", expand=True)
        ttk.Label(to_frame, text="To Format:").pack(anchor="w", pady=(0, 5))
        self.SINGLE_FORMAT_TO_BOX = ttk.Combobox(to_frame, state="readonly")
        self.SINGLE_FORMAT_TO_BOX.pack(fill="x")

        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill="x", pady=(15, 5))
        ttk.Label(output_frame, text="Output Folder:").pack(anchor="w", pady=(0, 5))

        output_row = ttk.Frame(output_frame)
        output_row.pack(fill="x")
        self.output_folder = tk.StringVar(value="")
        ttk.Entry(output_row, textvariable=self.output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_row, text="Browse",
                  command=lambda: self.controller.update_output_folder()).pack(side="right")

        # Action frame
        action_frame = ttk.Frame(single_frame)
        action_frame.pack(fill="x", pady=(10, 0))

        # Action buttons row
        buttons_frame = ttk.Frame(action_frame)
        buttons_frame.pack(fill="x", side="right")

        # Convert button
        ttk.Button(buttons_frame, text="Convert File", style="Accent.TButton",
                  command=lambda: self.controller.convert_single_files(self.file_paths)).pack(side="right")

        # --- Batch Conversion Tab ---
        batch_frame = ttk.Frame(notebook, padding=15)
        notebook.add(batch_frame, text="Batch Conversion")

        # Title with icon-like prefix
        ttk.Label(batch_frame, text="» Batch File Conversion",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # Short description
        ttk.Label(batch_frame, text="Convert multiple files of the same format in one operation.",
                 font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 10))

        # Batch file selection frame
        batch_file_frame = ttk.LabelFrame(batch_frame, text="Source Files", padding=15)
        batch_file_frame.pack(fill="x", pady=(0, 15))

        batch_file_row = ttk.Frame(batch_file_frame)
        batch_file_row.pack(fill="x", pady=5)
        self.batch_chosen_files = tk.StringVar(value="")
        self.batch_file_paths = []
        ttk.Entry(batch_file_row, textvariable=self.batch_chosen_files, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(batch_file_row, text="Browse Files", style="Accent.TButton",
                  command=lambda: self.controller.update_batch_chosen_files()).pack(side="right")

        # Batch conversion options
        batch_options_frame = ttk.LabelFrame(batch_frame, text="Conversion Options", padding=15)
        batch_options_frame.pack(fill="x", pady=(0, 15))

        batch_format_frame = ttk.Frame(batch_options_frame)
        batch_format_frame.pack(fill="x", pady=5)

        batch_from_frame = ttk.Frame(batch_format_frame)
        batch_from_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(batch_from_frame, text="From Format:").pack(anchor="w", pady=(0, 5))
        self.BATCH_FORMAT_FROM_BOX = ttk.Combobox(batch_from_frame, values=info.file_formats, state="readonly")
        self.BATCH_FORMAT_FROM_BOX.pack(fill="x")
        self.BATCH_FORMAT_FROM_BOX.bind('<<ComboboxSelected>>', lambda x: self.controller.update_batch_to_format())

        batch_to_frame = ttk.Frame(batch_format_frame)
        batch_to_frame.pack(side="right", fill="x", expand=True)
        ttk.Label(batch_to_frame, text="To Format:").pack(anchor="w", pady=(0, 5))
        self.BATCH_FORMAT_TO_BOX = ttk.Combobox(batch_to_frame, state="readonly")
        self.BATCH_FORMAT_TO_BOX.pack(fill="x")

        batch_output_frame = ttk.Frame(batch_options_frame)
        batch_output_frame.pack(fill="x", pady=(15, 5))
        ttk.Label(batch_output_frame, text="Output Folder:").pack(anchor="w", pady=(0, 5))

        batch_output_row = ttk.Frame(batch_output_frame)
        batch_output_row.pack(fill="x")
        self.batch_output_folder = tk.StringVar(value="")
        ttk.Entry(batch_output_row, textvariable=self.batch_output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(batch_output_row, text="Browse",
                  command=lambda: self.controller.update_batch_output_folder()).pack(side="right")

        # Batch action frame
        batch_action_frame = ttk.Frame(batch_frame)
        batch_action_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(batch_action_frame, text="Convert Files", style="Accent.TButton",
                  command=lambda: self.controller.convert_batch_files(self.batch_file_paths)).pack(side="right")

        # Add back button at the bottom
        ttk.Button(parent, text="Back", command=self.show_menu_page).pack(side="bottom", pady=10)

    def build_remove_bg_ui(self, parent):
        # UI elements for Remove Background functionality
        container = ttk.Frame(parent, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Remove Background from Images",
                  font=("Segoe UI", 14, "bold")).pack(anchor="center", pady=(0, 20))

        ttk.Label(container, text="Select image files to remove their backgrounds.",
                  font=("Segoe UI", 11)).pack(anchor="center", pady=5)

        # File selection frame
        file_frame = ttk.LabelFrame(container, text="Source Images", padding=15)
        file_frame.pack(fill="x", pady=(0, 15))

        file_row = ttk.Frame(file_frame)
        file_row.pack(fill="x", pady=5)
        self.bg_chosen_files = tk.StringVar(value="")
        self.bg_file_paths = []
        ttk.Entry(file_row, textvariable=self.bg_chosen_files, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(file_row, text="Browse Images", style="Accent.TButton",
                   command=lambda: self.controller.update_bg_chosen_files()).pack(side="right")

        # Output folder frame
        output_frame = ttk.Frame(container)
        output_frame.pack(fill="x", pady=(10, 0))
        ttk.Label(output_frame, text="Output Folder:").pack(anchor="w", pady=(0, 5))

        output_row = ttk.Frame(output_frame)
        output_row.pack(fill="x")
        self.bg_output_folder = tk.StringVar(value="")
        ttk.Entry(output_row, textvariable=self.bg_output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_row, text="Browse",
                  command=lambda: self.controller.update_bg_output_folder()).pack(side="right")

        # Action frame
        action_frame = ttk.Frame(container)
        action_frame.pack(fill="x", pady=(10, 0))

        # Action buttons row
        buttons_frame = ttk.Frame(action_frame)
        buttons_frame.pack(fill="x", side="right")

        # Remove Background button
        self.bg_remove_button = ttk.Button(buttons_frame, text="Remove Background", style="Accent.TButton",
                  command=lambda: self.controller.remove_background(self.bg_file_paths))
        self.bg_remove_button.pack(side="right")

        # Add back button at the bottom
        ttk.Button(parent, text="Back", command=self.show_menu_page).pack(side="bottom", pady=10)

        # Create a loading overlay that will be shown during processing
        self.loading_frame = ttk.Frame(self.ROOT, style="TFrame")
        self.loading_label = ttk.Label(
            self.loading_frame,
            text="Processing Images...\nPlease wait, this may take a few minutes.",
            font=("Segoe UI", 14),
            justify="center"
        )
        self.loading_label.pack(pady=20)
        self.loading_progress = ttk.Progressbar(
            self.loading_frame,
            orient="horizontal",
            mode="indeterminate",
            length=300
        )
        self.loading_progress.pack(pady=10)

    def show_loading_screen(self):
        """Show the loading overlay during background processing"""
        # Get the position of the main window
        x = self.ROOT.winfo_x() + (self.ROOT.winfo_width() // 4)
        y = self.ROOT.winfo_y() + (self.ROOT.winfo_height() // 4)

        # Position the loading window
        self.loading_frame.place(
            x=self.ROOT.winfo_width() // 4,
            y=self.ROOT.winfo_height() // 4,
            width=self.ROOT.winfo_width() // 2,
            height=self.ROOT.winfo_height() // 3,
            anchor="nw"
        )
        self.loading_frame.lift()
        self.loading_progress.start(10)
        self.ROOT.update()

    def hide_loading_screen(self):
        """Hide the loading overlay"""
        self.loading_progress.stop()
        self.loading_frame.place_forget()
        self.ROOT.update()

    def update_progress(self, value, max_value, message=""):
        """Update progress bar and optionally a status message"""
        if hasattr(self, 'BG_REMOVE_PROGRESS_BAR'):
            progress = int((value / max_value) * 100)
            self.BG_REMOVE_PROGRESS_BAR['value'] = progress
            if message and hasattr(self, 'bg_status_label'):
                self.bg_status_label.config(text=message)
            self.ROOT.update()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.ROOT.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.ROOT.attributes("-fullscreen", False)

    def set_controller(self, controller):
        self.controller = controller

    def lock_from_format(self):
        self.SINGLE_FORMAT_FROM_BOX.config(state="disabled")

    def unlock_from_format(self):
        self.SINGLE_FORMAT_FROM_BOX.config(state="readonly")

    def lock_batch_from_format(self):
        self.BATCH_FORMAT_FROM_BOX.config(state="disabled")

    def unlock_batch_from_format(self):
        self.BATCH_FORMAT_FROM_BOX.config(state="readonly")
