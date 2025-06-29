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

        # --- Image Editor Frame ---
        self.image_editor_frame = ttk.Frame(self.MAIN_FRAME)
        self.build_image_editor_ui(self.image_editor_frame)

        self.ROOT.bind("<F11>", self.toggle_fullscreen)
        self.ROOT.bind("<Escape>", self.exit_fullscreen)
        self.fullscreen = False

    def show_menu_page(self):
        self.conversion_frame.pack_forget()
        self.remove_bg_frame.pack_forget()
        self.about_frame.pack_forget()
        self.image_editor_frame.pack_forget()
        self.menu_page.pack(fill="both", expand=True)

    def show_conversion_frame(self):
        self.menu_page.pack_forget()
        self.about_frame.pack_forget()
        self.remove_bg_frame.pack_forget()
        self.image_editor_frame.pack_forget()
        self.conversion_frame.pack(fill="both", expand=True)

    def show_remove_background(self):
        self.menu_page.pack_forget()
        self.conversion_frame.pack_forget()
        self.about_frame.pack_forget()
        self.image_editor_frame.pack_forget()
        self.remove_bg_frame.pack(fill="both", expand=True)

    def show_about(self):
        self.menu_page.pack_forget()
        self.conversion_frame.pack_forget()
        self.remove_bg_frame.pack_forget()
        self.image_editor_frame.pack_forget()
        self.about_frame.pack(fill="both", expand=True)

    def show_image_editor_frame(self):
        self.menu_page.pack_forget()
        self.conversion_frame.pack_forget()
        self.remove_bg_frame.pack_forget()
        self.about_frame.pack_forget()
        self.image_editor_frame.pack(fill="both", expand=True)

    def build_image_editor_ui(self, parent):
        # Container for image editor tools
        editor_container = ttk.Frame(parent, padding=20)
        editor_container.pack(fill="both", expand=True)

        ttk.Label(editor_container, text="Image Editor",
                  font=("Segoe UI", 14, "bold")).pack(anchor="center", pady=(0, 10))

        # --- Notebook for different editing tools ---
        editor_notebook = ttk.Notebook(editor_container)
        editor_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Image Resizing Tab ---
        resize_frame = ttk.Frame(editor_notebook, padding=15)
        editor_notebook.add(resize_frame, text="Resize")
        self.build_resize_ui(resize_frame)

        # --- Image Compression Tab ---
        compress_frame = ttk.Frame(editor_notebook, padding=15)
        editor_notebook.add(compress_frame, text="Compress")
        self.build_compress_ui(compress_frame)

        # --- Color Adjustment Tab ---
        color_adjust_frame = ttk.Frame(editor_notebook, padding=15)
        editor_notebook.add(color_adjust_frame, text="Adjust Color")
        self.build_color_adjust_ui(color_adjust_frame)

        # --- Watermarking Tab ---
        watermark_frame = ttk.Frame(editor_notebook, padding=15)
        editor_notebook.add(watermark_frame, text="Watermark")
        self.build_watermark_ui(watermark_frame)

        # --- Metadata Tab ---
        metadata_frame = ttk.Frame(editor_notebook, padding=15)
        editor_notebook.add(metadata_frame, text="Metadata")
        self.build_metadata_ui(metadata_frame)

        # Add more tabs for other editing tools here later

        # Add back button at the bottom of the main parent frame for Image Editor
        ttk.Button(parent, text="Back", command=self.show_menu_page).pack(side="bottom", pady=10)


    def build_metadata_ui(self, parent_frame):
        # Title
        ttk.Label(parent_frame, text="» View & Edit Metadata",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # File selection
        file_frame = ttk.LabelFrame(parent_frame, text="Source Image", padding=15)
        file_frame.pack(fill="x", pady=(0, 10))
        file_row = ttk.Frame(file_frame)
        file_row.pack(fill="x", pady=5)
        self.metadata_chosen_file = tk.StringVar(value="")
        self.metadata_file_path = ""
        ttk.Entry(file_row, textvariable=self.metadata_chosen_file, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Button to load metadata
        ttk.Button(file_row, text="Load Image Metadata", style="Accent.TButton",
                   command=lambda: self.controller.load_image_metadata()).pack(side="right")

        # Metadata display and editing area
        metadata_area_frame = ttk.LabelFrame(parent_frame, text="Editable Metadata", padding=15)
        metadata_area_frame.pack(fill="both", expand=True, pady=(0,10))

        # For simplicity, we'll focus on a few common string tags.
        # A more complex UI would dynamically generate fields based on found EXIF data.

        self.metadata_fields = {} # To store StringVars for editable fields

        # Example: Artist/Author
        artist_frame = ttk.Frame(metadata_area_frame)
        artist_frame.pack(fill="x", pady=2)
        ttk.Label(artist_frame, text="Artist/Author:", width=15, anchor="w").pack(side="left", padx=5)
        self.metadata_fields["Artist"] = tk.StringVar()
        ttk.Entry(artist_frame, textvariable=self.metadata_fields["Artist"], width=50).pack(side="left", fill="x", expand=True, padx=5)

        # Example: Copyright
        copyright_frame = ttk.Frame(metadata_area_frame)
        copyright_frame.pack(fill="x", pady=2)
        ttk.Label(copyright_frame, text="Copyright:", width=15, anchor="w").pack(side="left", padx=5)
        self.metadata_fields["Copyright"] = tk.StringVar()
        ttk.Entry(copyright_frame, textvariable=self.metadata_fields["Copyright"], width=50).pack(side="left", fill="x", expand=True, padx=5)

        # Example: ImageDescription
        desc_frame = ttk.Frame(metadata_area_frame)
        desc_frame.pack(fill="x", pady=2)
        ttk.Label(desc_frame, text="Description:", width=15, anchor="w").pack(side="left", padx=5)
        self.metadata_fields["ImageDescription"] = tk.StringVar()
        ttk.Entry(desc_frame, textvariable=self.metadata_fields["ImageDescription"], width=50).pack(side="left", fill="x", expand=True, padx=5)

        # Non-editable metadata display (optional, could be a Text widget)
        # ttk.Label(metadata_area_frame, text="Full Metadata (View Only):").pack(anchor="w", pady=(10,2))
        # self.metadata_display_text = tk.Text(metadata_area_frame, height=10, width=60, state="disabled", wrap="word")
        # self.metadata_display_text.pack(fill="both", expand=True, pady=5)


        # Output folder (if saving a new copy, else could overwrite)
        # For now, let's assume saving a new copy to avoid accidental overwrites
        output_frame_meta = ttk.LabelFrame(parent_frame, text="Output Folder (for saving changes)", padding=15)
        output_frame_meta.pack(fill="x", pady=(0, 10))
        output_row_meta = ttk.Frame(output_frame_meta)
        output_row_meta.pack(fill="x")
        self.metadata_output_folder = tk.StringVar(value="")
        ttk.Entry(output_row_meta, textvariable=self.metadata_output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_row_meta, text="Browse",
                   command=lambda: self.controller.select_output_folder_for_editing("metadata")).pack(side="right")

        # Action button
        action_frame = ttk.Frame(parent_frame)
        action_frame.pack(fill="x", pady=(10,0))
        ttk.Button(action_frame, text="Save Metadata Changes", style="Accent.TButton",
                   command=lambda: self.controller.process_metadata_save()).pack(side="right")


    def build_watermark_ui(self, parent_frame):
        # Title
        ttk.Label(parent_frame, text="» Add Watermark",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # File selection for base image
        base_image_frame = ttk.LabelFrame(parent_frame, text="Base Image", padding=15)
        base_image_frame.pack(fill="x", pady=(0, 10))
        base_image_row = ttk.Frame(base_image_frame)
        base_image_row.pack(fill="x", pady=5)
        self.watermark_base_chosen_file = tk.StringVar(value="")
        self.watermark_base_file_path = ""
        ttk.Entry(base_image_row, textvariable=self.watermark_base_chosen_file, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(base_image_row, text="Browse Image", style="Accent.TButton",
                   command=lambda: self.controller.select_image_for_editing("watermark_base")).pack(side="right")

        # Watermark type selection
        watermark_type_frame = ttk.LabelFrame(parent_frame, text="Watermark Type", padding=15)
        watermark_type_frame.pack(fill="x", pady=(0,10))

        self.watermark_type_var = tk.StringVar(value="Text") # Default to Text
        text_radio = ttk.Radiobutton(watermark_type_frame, text="Text Watermark", variable=self.watermark_type_var, value="Text", command=self._toggle_watermark_options)
        text_radio.pack(anchor="w", side="left", padx=5)
        image_radio = ttk.Radiobutton(watermark_type_frame, text="Image Watermark", variable=self.watermark_type_var, value="Image", command=self._toggle_watermark_options)
        image_radio.pack(anchor="w", side="left", padx=5)

        # Text Watermark Options (initially visible or hidden based on selection)
        self.text_watermark_options_frame = ttk.LabelFrame(parent_frame, text="Text Watermark Options", padding=15)
        # self.text_watermark_options_frame.pack(fill="x", pady=(0,10)) # Packed by _toggle_watermark_options

        ttk.Label(self.text_watermark_options_frame, text="Text:").grid(row=0, column=0, sticky="w", pady=2, padx=5)
        self.watermark_text_var = tk.StringVar(value="Sample Watermark")
        ttk.Entry(self.text_watermark_options_frame, textvariable=self.watermark_text_var, width=40).grid(row=0, column=1, sticky="ew", pady=2, padx=5)

        # Basic font size (more complex font selection can be added later)
        ttk.Label(self.text_watermark_options_frame, text="Font Size:").grid(row=1, column=0, sticky="w", pady=2, padx=5)
        self.watermark_font_size_var = tk.IntVar(value=36)
        ttk.Entry(self.text_watermark_options_frame, textvariable=self.watermark_font_size_var, width=5).grid(row=1, column=1, sticky="w", pady=2, padx=5)
        # Color (simplified - hex code)
        # ttk.Label(self.text_watermark_options_frame, text="Color (hex):").grid(row=2, column=0, sticky="w", pady=2, padx=5)
        # self.watermark_text_color_var = tk.StringVar(value="#FFFFFF") # Default white
        # ttk.Entry(self.text_watermark_options_frame, textvariable=self.watermark_text_color_var, width=10).grid(row=2, column=1, sticky="w", pady=2, padx=5)


        # Image Watermark Options (initially hidden or visible)
        self.image_watermark_options_frame = ttk.LabelFrame(parent_frame, text="Image Watermark Options", padding=15)
        # self.image_watermark_options_frame.pack(fill="x", pady=(0,10)) # Packed by _toggle_watermark_options

        ttk.Label(self.image_watermark_options_frame, text="Watermark Image:").pack(anchor="w")
        self.watermark_image_chosen_file = tk.StringVar(value="")
        self.watermark_image_file_path = ""
        img_file_row = ttk.Frame(self.image_watermark_options_frame)
        img_file_row.pack(fill="x", pady=5)
        ttk.Entry(img_file_row, textvariable=self.watermark_image_chosen_file, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(img_file_row, text="Browse Watermark", style="Accent.TButton",
                   command=lambda: self.controller.select_image_for_editing("watermark_image")).pack(side="right")


        # Common Watermark Options (Opacity, Position)
        common_options_frame = ttk.LabelFrame(parent_frame, text="Common Options", padding=15)
        common_options_frame.pack(fill="x", pady=(0,10))

        # Opacity
        opacity_frame = ttk.Frame(common_options_frame)
        opacity_frame.pack(fill="x", pady=3)
        ttk.Label(opacity_frame, text="Opacity (0-1):").pack(side="left", padx=(0,5))
        self.watermark_opacity_var = tk.DoubleVar(value=0.5)
        opacity_scale = ttk.Scale(opacity_frame, from_=0.0, to=1.0, variable=self.watermark_opacity_var, orient="horizontal", length=150)
        opacity_scale.pack(side="left", padx=(0,10))
        ttk.Label(opacity_frame, textvariable=self.watermark_opacity_var, width=4).pack(side="left")
        opacity_scale.configure(command=lambda x: self.watermark_opacity_var.set(round(float(x), 2)))

        # Position
        pos_frame = ttk.Frame(common_options_frame)
        pos_frame.pack(fill="x", pady=3)
        ttk.Label(pos_frame, text="Position:").pack(side="left", padx=(0,5))
        self.watermark_position_var = tk.StringVar(value="center")
        positions = ["center", "top-left", "top-right", "bottom-left", "bottom-right", "tile"]
        ttk.Combobox(pos_frame, textvariable=self.watermark_position_var, values=positions, state="readonly", width=15).pack(side="left")

        # Output folder
        output_frame_watermark = ttk.LabelFrame(parent_frame, text="Output Folder", padding=15)
        output_frame_watermark.pack(fill="x", pady=(10, 10))
        output_row_watermark = ttk.Frame(output_frame_watermark)
        output_row_watermark.pack(fill="x")
        self.watermark_output_folder = tk.StringVar(value="")
        ttk.Entry(output_row_watermark, textvariable=self.watermark_output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_row_watermark, text="Browse",
                   command=lambda: self.controller.select_output_folder_for_editing("watermark")).pack(side="right")

        # Action button
        action_frame = ttk.Frame(parent_frame)
        action_frame.pack(fill="x", pady=(10,0))
        ttk.Button(action_frame, text="Apply Watermark", style="Accent.TButton",
                   command=lambda: self.controller.process_watermark_application()).pack(side="right")

        self._toggle_watermark_options() # Call to set initial visibility


    def _toggle_watermark_options(self):
        if self.watermark_type_var.get() == "Text":
            self.text_watermark_options_frame.pack(fill="x", pady=(0,10), before=self.image_watermark_options_frame)
            self.image_watermark_options_frame.pack_forget()
        else: # Image
            self.image_watermark_options_frame.pack(fill="x", pady=(0,10), before=self.text_watermark_options_frame)
            self.text_watermark_options_frame.pack_forget()


    def build_color_adjust_ui(self, parent_frame):
        # Title
        ttk.Label(parent_frame, text="» Color Adjustments & Filters",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # File selection
        file_frame = ttk.LabelFrame(parent_frame, text="Source Image", padding=15)
        file_frame.pack(fill="x", pady=(0, 10))
        file_row = ttk.Frame(file_frame)
        file_row.pack(fill="x", pady=5)
        self.color_chosen_file = tk.StringVar(value="")
        self.color_file_path = ""
        ttk.Entry(file_row, textvariable=self.color_chosen_file, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(file_row, text="Browse Image", style="Accent.TButton",
                   command=lambda: self.controller.select_image_for_editing("color_adjust")).pack(side="right")

        # Adjustment options
        options_frame = ttk.LabelFrame(parent_frame, text="Adjustment Options", padding=15)
        options_frame.pack(fill="x", pady=(0, 10))

        # Brightness
        bright_frame = ttk.Frame(options_frame)
        bright_frame.pack(fill="x", pady=3)
        ttk.Label(bright_frame, text="Brightness:").pack(side="left", padx=(0,5), anchor="w")
        self.brightness_var = tk.DoubleVar(value=1.0) # 1.0 is no change
        bright_scale = ttk.Scale(bright_frame, from_=0.0, to=2.0, variable=self.brightness_var, orient="horizontal", length=180)
        bright_scale.pack(side="left", padx=(0,10))
        ttk.Label(bright_frame, textvariable=self.brightness_var, width=4).pack(side="left")
        bright_scale.configure(command=lambda x: self.brightness_var.set(round(float(x), 2)))


        # Contrast
        contrast_frame = ttk.Frame(options_frame)
        contrast_frame.pack(fill="x", pady=3)
        ttk.Label(contrast_frame, text="Contrast:    ").pack(side="left", padx=(0,5), anchor="w") # Added spaces for alignment
        self.contrast_var = tk.DoubleVar(value=1.0) # 1.0 is no change
        contrast_scale = ttk.Scale(contrast_frame, from_=0.0, to=2.0, variable=self.contrast_var, orient="horizontal", length=180)
        contrast_scale.pack(side="left", padx=(0,10))
        ttk.Label(contrast_frame, textvariable=self.contrast_var, width=4).pack(side="left")
        contrast_scale.configure(command=lambda x: self.contrast_var.set(round(float(x), 2)))

        # Saturation
        sat_frame = ttk.Frame(options_frame)
        sat_frame.pack(fill="x", pady=3)
        ttk.Label(sat_frame, text="Saturation:").pack(side="left", padx=(0,5), anchor="w")
        self.saturation_var = tk.DoubleVar(value=1.0) # 1.0 is no change
        sat_scale = ttk.Scale(sat_frame, from_=0.0, to=2.0, variable=self.saturation_var, orient="horizontal", length=180)
        sat_scale.pack(side="left", padx=(0,10))
        ttk.Label(sat_frame, textvariable=self.saturation_var, width=4).pack(side="left")
        sat_scale.configure(command=lambda x: self.saturation_var.set(round(float(x), 2)))

        # Filters
        filter_frame = ttk.Frame(options_frame)
        filter_frame.pack(fill="x", pady=(10,3))
        ttk.Label(filter_frame, text="Filter:         ").pack(side="left", padx=(0,5), anchor="w") # Added spaces for alignment
        self.filter_var = tk.StringVar(value="None")
        filter_options = ["None", "Grayscale", "Sepia"] # Add more later if needed
        filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly", width=15)
        filter_menu.pack(side="left")

        # Output folder
        output_frame_color = ttk.LabelFrame(parent_frame, text="Output Folder", padding=15)
        output_frame_color.pack(fill="x", pady=(10, 10))
        output_row_color = ttk.Frame(output_frame_color)
        output_row_color.pack(fill="x")
        self.color_output_folder = tk.StringVar(value="")
        ttk.Entry(output_row_color, textvariable=self.color_output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_row_color, text="Browse",
                   command=lambda: self.controller.select_output_folder_for_editing("color_adjust")).pack(side="right")

        # Action button
        action_frame = ttk.Frame(parent_frame)
        action_frame.pack(fill="x", pady=(10,0))
        ttk.Button(action_frame, text="Apply Adjustments", style="Accent.TButton",
                   command=lambda: self.controller.process_color_adjustment()).pack(side="right")


    def build_compress_ui(self, parent_frame):
        # Title
        ttk.Label(parent_frame, text="» Image Compression",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # File selection
        file_frame = ttk.LabelFrame(parent_frame, text="Source Image", padding=15)
        file_frame.pack(fill="x", pady=(0, 10))
        file_row = ttk.Frame(file_frame)
        file_row.pack(fill="x", pady=5)
        self.compress_chosen_file = tk.StringVar(value="")
        self.compress_file_path = "" # Store single file path
        ttk.Entry(file_row, textvariable=self.compress_chosen_file, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(file_row, text="Browse Image", style="Accent.TButton",
                   command=lambda: self.controller.select_image_for_editing("compress")).pack(side="right")

        # Compression options
        options_frame = ttk.LabelFrame(parent_frame, text="Compression Options", padding=15)
        options_frame.pack(fill="x", pady=(0, 10))

        # Quality slider (for JPEG/WEBP)
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill="x", pady=5)
        ttk.Label(quality_frame, text="Quality (1-100):").pack(side="left", padx=(0,5))
        self.compress_quality_var = tk.IntVar(value=85) # Default quality
        quality_scale = ttk.Scale(quality_frame, from_=1, to=100, variable=self.compress_quality_var, orient="horizontal", length=200)
        quality_scale.pack(side="left", padx=(0,10))
        # Display current quality value
        quality_value_label = ttk.Label(quality_frame, textvariable=self.compress_quality_var)
        quality_value_label.pack(side="left")
        # Set the command to update the label after the scale is created
        quality_scale.configure(command=lambda x: self.compress_quality_var.set(int(float(x))))


        # Output folder
        output_frame_compress = ttk.LabelFrame(parent_frame, text="Output Folder", padding=15)
        output_frame_compress.pack(fill="x", pady=(0, 10))
        output_row_compress = ttk.Frame(output_frame_compress)
        output_row_compress.pack(fill="x")
        self.compress_output_folder = tk.StringVar(value="")
        ttk.Entry(output_row_compress, textvariable=self.compress_output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_row_compress, text="Browse",
                   command=lambda: self.controller.select_output_folder_for_editing("compress")).pack(side="right")

        # Action button
        action_frame = ttk.Frame(parent_frame)
        action_frame.pack(fill="x", pady=(10,0))
        ttk.Button(action_frame, text="Compress Image", style="Accent.TButton",
                   command=lambda: self.controller.process_image_compression()).pack(side="right")


    def build_resize_ui(self, parent_frame):
        # Title
        ttk.Label(parent_frame, text="» Image Resizing",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # File selection
        file_frame = ttk.LabelFrame(parent_frame, text="Source Image", padding=15)
        file_frame.pack(fill="x", pady=(0, 10))
        file_row = ttk.Frame(file_frame)
        file_row.pack(fill="x", pady=5)
        self.resize_chosen_file = tk.StringVar(value="")
        self.resize_file_path = "" # Store single file path
        ttk.Entry(file_row, textvariable=self.resize_chosen_file, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(file_row, text="Browse Image", style="Accent.TButton",
                   command=lambda: self.controller.select_image_for_editing("resize")).pack(side="right") # Modified command

        # Resizing options
        options_frame = ttk.LabelFrame(parent_frame, text="Resizing Options", padding=15)
        options_frame.pack(fill="x", pady=(0, 10))

        # Dimensions
        dim_frame = ttk.Frame(options_frame)
        dim_frame.pack(fill="x", pady=5)
        ttk.Label(dim_frame, text="Width (px):").pack(side="left", padx=(0,5))
        self.resize_width_var = tk.StringVar()
        ttk.Entry(dim_frame, textvariable=self.resize_width_var, width=7).pack(side="left", padx=(0,10))
        ttk.Label(dim_frame, text="Height (px):").pack(side="left", padx=(0,5))
        self.resize_height_var = tk.StringVar()
        ttk.Entry(dim_frame, textvariable=self.resize_height_var, width=7).pack(side="left", padx=(0,10))

        # Percentage
        perc_frame = ttk.Frame(options_frame)
        perc_frame.pack(fill="x", pady=5)
        ttk.Label(perc_frame, text="Scale (%):").pack(side="left", padx=(0,5))
        self.resize_percentage_var = tk.StringVar()
        ttk.Entry(perc_frame, textvariable=self.resize_percentage_var, width=7).pack(side="left", padx=(0,10))

        # Keep aspect ratio
        self.resize_keep_aspect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Keep Aspect Ratio", variable=self.resize_keep_aspect_var).pack(anchor="w", pady=5)

        # Output folder
        output_frame_resize = ttk.LabelFrame(parent_frame, text="Output Folder", padding=15)
        output_frame_resize.pack(fill="x", pady=(0, 10))
        output_row_resize = ttk.Frame(output_frame_resize)
        output_row_resize.pack(fill="x")
        self.resize_output_folder = tk.StringVar(value="")
        ttk.Entry(output_row_resize, textvariable=self.resize_output_folder, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(output_row_resize, text="Browse",
                   command=lambda: self.controller.select_output_folder_for_editing("resize")).pack(side="right")


        # Action button
        action_frame = ttk.Frame(parent_frame)
        action_frame.pack(fill="x", pady=(10,0))
        ttk.Button(action_frame, text="Resize Image", style="Accent.TButton",
                   command=lambda: self.controller.process_image_resize()).pack(side="right")


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
