from tkinter import filedialog
from tkinter import messagebox as mb
import Conversions as info
import os

class FileHandler:
    def __init__(self, controller):
        self.controller = controller
        self.gui = None

    def set_gui(self, gui):
        self.gui = gui

    def update_to_format(self):
        from_format = self.gui.SINGLE_FORMAT_FROM_BOX.get()
        to_format = self.gui.SINGLE_FORMAT_TO_BOX
        if from_format in info.conversions:
            to_format['values'] = info.conversions[from_format]
        else:
            mb.showerror("Unrecognized Type", "You have selected a file type that is not recognized. How did you do that?")

    def update_chosen_file(self):
        input_path = filedialog.askopenfilename()
        if input_path:
            print("path chosen", input_path)
            self.gui.chosen_file.set(os.path.basename(input_path))
            self.gui.file_path = input_path

            ext = os.path.splitext(input_path)[1].lstrip('.').upper()
            if ext in info.file_formats:
                self.gui.SINGLE_FORMAT_FROM_BOX.set(ext)
                self.update_to_format()
                self.gui.lock_from_format()
            else:
                self.gui.SINGLE_FORMAT_FROM_BOX.set('')
                self.gui.unlock_from_format()

            self.gui.output_folder.set(os.path.dirname(input_path))
        else:
            self.gui.chosen_file.set("")
            self.gui.file_path = ""
            self.gui.SINGLE_FORMAT_FROM_BOX.set('')
            self.gui.unlock_from_format()

    def update_chosen_files(self):
        input_paths = filedialog.askopenfilenames()
        if input_paths:
            file_names = [os.path.basename(p) for p in input_paths]
            self.gui.chosen_files.set(", ".join(file_names))
            self.gui.file_paths = list(input_paths)

            ext = os.path.splitext(input_paths[0])[1].lstrip('.').upper()
            if ext in info.file_formats:
                self.gui.SINGLE_FORMAT_FROM_BOX.set(ext)
                self.update_to_format()
                self.gui.lock_from_format()
            else:
                self.gui.SINGLE_FORMAT_FROM_BOX.set('')
                self.gui.unlock_from_format()
            self.gui.output_folder.set(os.path.dirname(input_paths[0]))
        else:
            self.gui.chosen_files.set("")
            self.gui.file_paths = []
            self.gui.SINGLE_FORMAT_FROM_BOX.set('')
            self.gui.unlock_from_format()

    def update_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.gui.output_folder.set(folder_path)

    def update_batch_to_format(self):
        from_format = self.gui.BATCH_FORMAT_FROM_BOX.get()
        to_format = self.gui.BATCH_FORMAT_TO_BOX
        if from_format in info.conversions:
            to_format['values'] = info.conversions[from_format]
        else:
            mb.showerror("Unrecognized Type", "You have selected a file type that is not recognized. How did you do that?")

    def update_batch_chosen_files(self):
        input_paths = filedialog.askopenfilenames()
        if input_paths:
            exts = [os.path.splitext(p)[1].lstrip('.').upper() for p in input_paths]
            if len(set(exts)) != 1:
                mb.showerror("Format Mismatch", "All selected files must have the same format.")
                self.gui.batch_chosen_files.set("")
                self.gui.batch_file_paths = []
                self.gui.BATCH_FORMAT_FROM_BOX.set('')
                self.gui.unlock_batch_from_format()
                return
            file_names = [os.path.basename(p) for p in input_paths]
            self.gui.batch_chosen_files.set(", ".join(file_names))
            self.gui.batch_file_paths = list(input_paths)

            ext = exts[0]
            if ext in info.file_formats:
                self.gui.BATCH_FORMAT_FROM_BOX.set(ext)
                self.update_batch_to_format()
                self.gui.lock_batch_from_format()
            else:
                self.gui.BATCH_FORMAT_FROM_BOX.set('')
                self.gui.unlock_batch_from_format()
            self.gui.batch_output_folder.set(os.path.dirname(input_paths[0]))
        else:
            self.gui.batch_chosen_files.set("")
            self.gui.batch_file_paths = []
            self.gui.BATCH_FORMAT_FROM_BOX.set('')
            self.gui.unlock_batch_from_format()

    def update_batch_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.gui.batch_output_folder.set(folder_path)

    def update_bg_chosen_files(self):
        """Browse and select image files for background removal"""
        input_paths = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.gif")]
        )
        if input_paths:
            file_names = [os.path.basename(p) for p in input_paths]
            self.gui.bg_chosen_files.set(", ".join(file_names))
            self.gui.bg_file_paths = list(input_paths)

            # Set the output folder to the same directory as the first selected file
            if not self.gui.bg_output_folder.get():
                self.gui.bg_output_folder.set(os.path.dirname(input_paths[0]))
        else:
            self.gui.bg_chosen_files.set("")
            self.gui.bg_file_paths = []

    def update_bg_output_folder(self):
        """Browse and select the output folder for background-removed images"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.gui.bg_output_folder.set(folder_path)
