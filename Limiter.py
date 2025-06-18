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
