from tkinter import messagebox as mb
from FileHandler import FileHandler
from Converter import Converter
from BackgroundRemover import BackgroundRemover

class Controller:
    def __init__(self) -> None:
        # Initialize the component handlers
        self.file_handler = FileHandler(self)
        self.converter = Converter(self)
        self.bg_remover = BackgroundRemover(self)
        self.gui = None

    def set_gui(self, gui):
        self.gui = gui
        # Pass the GUI reference to all components
        self.file_handler.set_gui(gui)
        self.converter.set_gui(gui)
        self.bg_remover.set_gui(gui)
        self.bg_remover.set_converter(self.converter)
    
    # FileHandler methods
    def update_to_format(self):
        return self.file_handler.update_to_format()
    
    def update_chosen_file(self):
        return self.file_handler.update_chosen_file()
    
    def update_chosen_files(self):
        return self.file_handler.update_chosen_files()
    
    def update_output_folder(self):
        return self.file_handler.update_output_folder()
    
    def update_batch_to_format(self):
        return self.file_handler.update_batch_to_format()
    
    def update_batch_chosen_files(self):
        return self.file_handler.update_batch_chosen_files()
    
    def update_batch_output_folder(self):
        return self.file_handler.update_batch_output_folder()
    
    def update_bg_chosen_files(self):
        return self.file_handler.update_bg_chosen_files()
    
    def update_bg_output_folder(self):
        return self.file_handler.update_bg_output_folder()
    
    # Converter methods
    def convert_single_file(self, file_path):
        return self.converter.convert_single_file(file_path)
    
    def convert_single_files(self, file_paths):
        return self.converter.convert_single_files(file_paths)
    
    def convert_batch_files(self, file_paths):
        return self.converter.convert_batch_files(file_paths)
    
    def check_allowed_conversion(self, from_format, to_format):
        return self.converter.check_allowed_conversion(from_format, to_format)
    
    def is_image_format(self, fmt):
        return self.converter.is_image_format(fmt)
    
    def is_audio_format(self, fmt):
        return self.converter.is_audio_format(fmt)
    
    # BackgroundRemover methods
    def remove_background(self, file_paths):
        return self.bg_remover.remove_background(file_paths)

    # Image Editor methods
    def select_image_for_editing(self, editor_type):
        return self.file_handler.select_image_for_editing(editor_type)

    def select_output_folder_for_editing(self, editor_type):
        return self.file_handler.select_output_folder_for_editing(editor_type)

    def process_image_resize(self):
        file_path = self.gui.resize_file_path
        output_folder = self.gui.resize_output_folder.get()
        width_str = self.gui.resize_width_var.get()
        height_str = self.gui.resize_height_var.get()
        percentage_str = self.gui.resize_percentage_var.get()
        keep_aspect_ratio = self.gui.resize_keep_aspect_var.get()

        if not file_path:
            mb.showerror("Error", "Please select an image file.")
            return
        if not output_folder:
            mb.showerror("Error", "Please select an output folder.")
            return

        width, height, percentage = None, None, None
        try:
            if percentage_str:
                percentage = float(percentage_str)
                if percentage <= 0:
                    mb.showerror("Error", "Percentage must be greater than 0.")
                    return
            elif width_str or height_str:
                if width_str:
                    width = int(width_str)
                    if width <= 0:
                        mb.showerror("Error", "Width must be greater than 0.")
                        return
                if height_str:
                    height = int(height_str)
                    if height <= 0:
                        mb.showerror("Error", "Height must be greater than 0.")
                        return
            else:
                mb.showerror("Error", "Please specify resize dimensions or percentage.")
                return
        except ValueError:
            mb.showerror("Error", "Invalid input for dimensions or percentage. Please enter numbers only.")
            return

        # Call converter method (to be created)
        self.converter.resize_image_thread(file_path, output_folder, width, height, percentage, keep_aspect_ratio)

    def process_image_compression(self):
        file_path = self.gui.compress_file_path
        output_folder = self.gui.compress_output_folder.get()
        quality = self.gui.compress_quality_var.get()

        if not file_path:
            mb.showerror("Error", "Please select an image file.")
            return
        if not output_folder:
            mb.showerror("Error", "Please select an output folder.")
            return

        if not 1 <= quality <= 100:
            mb.showerror("Error", "Quality must be between 1 and 100.")
            return

        # Call converter method (to be created)
        self.converter.compress_image_thread(file_path, output_folder, quality)

    def process_color_adjustment(self):
        file_path = self.gui.color_file_path
        output_folder = self.gui.color_output_folder.get()
        brightness = self.gui.brightness_var.get()
        contrast = self.gui.contrast_var.get()
        saturation = self.gui.saturation_var.get()
        selected_filter = self.gui.filter_var.get()

        if not file_path:
            mb.showerror("Error", "Please select an image file.")
            return
        if not output_folder:
            mb.showerror("Error", "Please select an output folder.")
            return

        # Call converter method (to be created)
        self.converter.adjust_color_thread(file_path, output_folder, brightness, contrast, saturation, selected_filter)

    def process_watermark_application(self):
        base_image_path = self.gui.watermark_base_file_path
        output_folder = self.gui.watermark_output_folder.get()

        watermark_type = self.gui.watermark_type_var.get()
        text_content = self.gui.watermark_text_var.get()
        font_size = self.gui.watermark_font_size_var.get()
        # text_color = self.gui.watermark_text_color_var.get() # If color picker added
        watermark_image_path = self.gui.watermark_image_file_path

        opacity = self.gui.watermark_opacity_var.get()
        position = self.gui.watermark_position_var.get()

        if not base_image_path:
            mb.showerror("Error", "Please select a base image.")
            return
        if not output_folder:
            mb.showerror("Error", "Please select an output folder.")
            return

        if watermark_type == "Text":
            if not text_content:
                mb.showerror("Error", "Please enter watermark text.")
                return
            try:
                if int(font_size) <=0:
                    mb.showerror("Error", "Font size must be positive.")
                    return
            except ValueError:
                mb.showerror("Error", "Invalid font size.")
                return
        elif watermark_type == "Image":
            if not watermark_image_path:
                mb.showerror("Error", "Please select a watermark image.")
                return

        # Call converter method (to be created)
        self.converter.apply_watermark_thread(
            base_image_path, output_folder, watermark_type,
            text_content, font_size, # text_color,
            watermark_image_path, opacity, position
        )

    def load_image_metadata(self):
        # First, ensure a file is selected using the generic file selection method
        self.file_handler.select_image_for_editing("metadata")
        file_path = self.gui.metadata_file_path

        if not file_path:
            # select_image_for_editing would have cleared path if user cancelled dialog
            # No error message needed here as select_image_for_editing doesn't show one for cancel
            return

        metadata = self.converter.read_metadata(file_path)
        if metadata is None: # Error handled by converter.read_metadata
            return

        # Populate GUI fields
        for key, var in self.gui.metadata_fields.items():
            var.set(metadata.get(key, "")) # Get value or empty string if key not present

        # Optionally, display full metadata in a text box if implemented
        # full_metadata_str = "\n".join(f"{k}: {v}" for k, v in metadata.items())
        # self.gui.metadata_display_text.config(state="normal")
        # self.gui.metadata_display_text.delete(1.0, tk.END)
        # self.gui.metadata_display_text.insert(tk.END, full_metadata_str)
        # self.gui.metadata_display_text.config(state="disabled")
        mb.showinfo("Metadata Loaded", "Editable metadata fields have been populated. Full EXIF data can be extensive and is not fully shown here.")


    def process_metadata_save(self):
        file_path = self.gui.metadata_file_path
        output_folder = self.gui.metadata_output_folder.get()

        if not file_path:
            mb.showerror("Error", "Please load an image first.")
            return
        if not output_folder:
            mb.showerror("Error", "Please select an output folder.")
            return

        updated_metadata = {}
        for key, var in self.gui.metadata_fields.items():
            updated_metadata[key] = var.get()

        self.converter.edit_metadata_thread(file_path, output_folder, updated_metadata)
