from tkinter import messagebox as mb
import Conversions as info
import os
import shutil
import subprocess
import threading
import time

class Converter:
    def __init__(self, controller):
        self.controller = controller
        self.gui = None

    def set_gui(self, gui):
        self.gui = gui

    def check_file_name(self, file_path, increment, to_format, output_folder=None):
        base_name = os.path.basename(file_path)
        base, ext = os.path.splitext(base_name)
        print(base, ext)
        suffix = f"_{increment}" if increment != 0 else ""
        if output_folder:
            out_path = os.path.join(output_folder, f"{base}{suffix}.{to_format}")
        else:
            out_path = f"{base}{suffix}.{to_format}"
        if os.path.exists(out_path):
            print("Path exists", increment)
            return self.check_file_name(file_path=file_path, increment=increment + 1, to_format=to_format, output_folder=output_folder)
        else:
            return out_path

    def check_allowed_conversion(self, from_format, to_format):
        if from_format in info.conversions:
            if to_format in info.conversions[from_format]:
                return True
            else:
                return False
        else:
            return False

    def is_image_format(self, fmt):
        return fmt.upper() in ["PNG", "JPG", "JPEG", "GIF", "BMP", "WEBP", "TIFF"]

    def is_audio_format(self, fmt):
        return fmt.upper() in ["MP3", "WAV", "AAC", "OGG", "FLAC"]

    def convert_single_file(self, file_path):
        chosen_from_format = self.gui.SINGLE_FORMAT_FROM_BOX.get()
        chosen_to_format = self.gui.SINGLE_FORMAT_TO_BOX.get()
        output_folder = self.gui.output_folder.get()
        if file_path != "":
            if chosen_to_format != "":
                if self.check_allowed_conversion(chosen_from_format,chosen_to_format):
                    if self.is_image_format(chosen_from_format) and self.is_image_format(chosen_to_format):
                        self.convert_image(file_path, chosen_to_format, output_folder)
                    elif self.is_audio_format(chosen_from_format) and self.is_audio_format(chosen_to_format):
                        self.convert_audio(file_path, chosen_to_format, output_folder)
                    else:
                        mb.showerror("Conversion not supported", "Only image and audio conversions are supported without ffmpeg.")
                else:
                    mb.showerror("Conversion not allowed", "This conversion is not supported. How did you do this?")
            else:
                mb.showerror("No Output Selected", "There is no output format selected. Please select an output format before trying to convert.")
        else:
            mb.showerror("No File Selected","There is no file selected. Please select a file before trying to convert.")

    def convert_single_files(self, file_paths):
        chosen_from_format = self.gui.SINGLE_FORMAT_FROM_BOX.get()
        chosen_to_format = self.gui.SINGLE_FORMAT_TO_BOX.get()
        output_folder = self.gui.output_folder.get()
        if file_paths and len(file_paths) > 0:
            if chosen_to_format != "":
                if self.check_allowed_conversion(chosen_from_format, chosen_to_format):
                    # Create a separate thread for conversion processing
                    process_thread = threading.Thread(
                        target=self._process_single_files_conversion,
                        args=(file_paths, chosen_from_format, chosen_to_format, output_folder)
                    )
                    process_thread.daemon = True  # Thread will exit when main program exits

                    # Start the thread and show loading screen
                    self.gui.show_loading_screen()
                    process_thread.start()
                else:
                    mb.showerror("Conversion not allowed", "This conversion is not supported. How did you do this?")
            else:
                mb.showerror("No Output Selected", "There is no output format selected. Please select an output format before trying to convert.")
        else:
            mb.showerror("No File Selected", "There are no files selected. Please select files before trying to convert.")

    def _process_single_files_conversion(self, file_paths, from_format, to_format, output_folder):
        """Process file conversion in a separate thread"""
        try:
            total_files = len(file_paths)
            successful_files = 0

            for i, file_path in enumerate(file_paths):
                # Update progress indicator
                file_name = os.path.basename(file_path)
                self.gui.update_progress(i, total_files, f"Converting {file_name}...")

                try:
                    if self.is_image_format(from_format) and self.is_image_format(to_format):
                        out_path = self._convert_image_file(file_path, to_format, output_folder)
                        successful_files += 1
                    elif self.is_audio_format(from_format) and self.is_audio_format(to_format):
                        out_path = self._convert_audio_file(file_path, to_format, output_folder)
                        successful_files += 1
                    else:
                        self.gui.ROOT.after(100, lambda: mb.showerror("Conversion not supported", "Only image and audio conversions are supported without ffmpeg."))
                        break
                except Exception as file_error:
                    print(f"Error converting {file_name}: {file_error}")
                    continue

            # Update final progress
            self.gui.update_progress(total_files, total_files, f"Completed! Converted {successful_files} of {total_files} files.")

            # Show success message
            if successful_files > 0:
                self.gui.ROOT.after(500, lambda: mb.showinfo("Success", f"Conversion completed successfully! Converted {successful_files} of {total_files} files."))
            else:
                self.gui.ROOT.after(500, lambda: mb.showerror("Error", "Failed to convert any files."))

        except Exception as e:
            # Show error message
            self.gui.ROOT.after(500, lambda: mb.showerror("Error", f"An error occurred during conversion:\n{e}"))

        finally:
            # Hide loading screen
            self.gui.ROOT.after(100, self.gui.hide_loading_screen)

    def _convert_image_file(self, file_path, to_format, output_folder):
        """Convert a single image file and return the output path"""
        out_path = self.check_file_name(file_path, increment=0, to_format=to_format.lower(), output_folder=output_folder)
        # Use ffmpeg for image conversion if available, else just copy and rename
        if shutil.which("ffmpeg"):
            subprocess.run([
                "ffmpeg", "-y", "-i", file_path, out_path
            ], check=True)
        else:
            shutil.copy(file_path, out_path)
        return out_path

    def _convert_audio_file(self, file_path, to_format, output_folder):
        """Convert a single audio file and return the output path"""
        if not shutil.which("ffmpeg"):
            raise Exception("FFmpeg Not Found. Audio conversion requires FFmpeg, which was not found in your system PATH.")

        out_path = self.check_file_name(file_path, increment=0, to_format=to_format.lower(), output_folder=output_folder)
        subprocess.run([
            "ffmpeg", "-y", "-i", file_path, out_path
        ], check=True)
        return out_path

    def convert_image(self, file_path, to_format, output_folder):
        try:
            out_path = self.check_file_name(file_path, increment=0, to_format=to_format.lower(), output_folder=output_folder)
            # Use ffmpeg for image conversion if available, else just copy and rename
            if shutil.which("ffmpeg"):
                subprocess.run([
                    "ffmpeg", "-y", "-i", file_path, out_path
                ], check=True)
            else:
                shutil.copy(file_path, out_path)
            mb.showinfo("Success", f"Image converted and saved to {out_path}")
        except Exception as e:
            mb.showerror("Error", f"An Error Has occured:\n{e}")

    def convert_audio(self, file_path, to_format, output_folder):
        try:
            if not shutil.which("ffmpeg"):
                mb.showerror(
                    "FFmpeg Not Found",
                    "Audio conversion requires FFmpeg, which was not found in your system PATH. Please install FFmpeg and ensure it is accessible from the command line."
                )
                return
            out_path = self.check_file_name(file_path, increment=0, to_format=to_format.lower(), output_folder=output_folder)
            subprocess.run([
                "ffmpeg", "-y", "-i", file_path, out_path
            ], check=True)
            mb.showinfo("Success", f"Audio converted and saved to {out_path}")
        except Exception as e:
            mb.showerror("Error", f"An Error Has occured:\n{e}")

    def convert_batch_files(self, file_paths):
        chosen_from_format = self.gui.BATCH_FORMAT_FROM_BOX.get()
        chosen_to_format = self.gui.BATCH_FORMAT_TO_BOX.get()
        output_folder = self.gui.batch_output_folder.get()
        if file_paths and len(file_paths) > 0:
            if chosen_to_format != "":
                if self.check_allowed_conversion(chosen_from_format, chosen_to_format):
                    out_folder_name = "[original image format] [export image format]"
                    out_folder_name = out_folder_name.replace(
                        "[original image format]", chosen_from_format.lower()
                    ).replace(
                        "[export image format]", chosen_to_format.lower()
                    )
                    out_folder_path = os.path.join(output_folder, out_folder_name)
                    os.makedirs(out_folder_path, exist_ok=True)

                    # Create a separate thread for batch conversion processing
                    process_thread = threading.Thread(
                        target=self._process_batch_files_conversion,
                        args=(file_paths, chosen_from_format, chosen_to_format, out_folder_path)
                    )
                    process_thread.daemon = True  # Thread will exit when main program exits

                    # Start the thread and show loading screen
                    self.gui.show_loading_screen()
                    process_thread.start()
                else:
                    mb.showerror("Conversion not allowed", "This conversion is not supported. How did you do this?")
            else:
                mb.showerror("No Output Selected", "There is no output format selected. Please select an output format before trying to convert.")
        else:
            mb.showerror("No File Selected", "There are no files selected. Please select files before trying to convert.")

    def _process_batch_files_conversion(self, file_paths, from_format, to_format, out_folder_path):
        """Process batch file conversion in a separate thread"""
        try:
            total_files = len(file_paths)
            successful_files = 0

            for i, file_path in enumerate(file_paths):
                # Update progress indicator
                file_name = os.path.basename(file_path)
                self.gui.update_progress(i, total_files, f"Converting {file_name}...")

                try:
                    if self.is_image_format(from_format) and self.is_image_format(to_format):
                        base = os.path.splitext(os.path.basename(file_path))[0]
                        out_path = os.path.join(out_folder_path, f"{base}.{to_format.lower()}")

                        if shutil.which("ffmpeg"):
                            subprocess.run([
                                "ffmpeg", "-y", "-i", file_path, out_path
                            ], check=True)
                        else:
                            shutil.copy(file_path, out_path)
                        successful_files += 1
                    elif self.is_audio_format(from_format) and self.is_audio_format(to_format):
                        if not shutil.which("ffmpeg"):
                            raise Exception("FFmpeg Not Found. Audio conversion requires FFmpeg, which was not found in your system PATH.")

                        base = os.path.splitext(os.path.basename(file_path))[0]
                        out_path = os.path.join(out_folder_path, f"{base}.{to_format.lower()}")
                        subprocess.run([
                            "ffmpeg", "-y", "-i", file_path, out_path
                        ], check=True)
                        successful_files += 1
                    else:
                        self.gui.ROOT.after(100, lambda: mb.showerror(
                            "Conversion not supported",
                            "Only image and audio batch conversions are supported without ffmpeg."
                        ))
                        break
                except Exception as file_error:
                    print(f"Error converting {file_name}: {file_error}")
                    continue

            # Update final progress
            self.gui.update_progress(total_files, total_files, f"Completed! Converted {successful_files} of {total_files} files.")

            # Show success message
            if successful_files > 0:
                self.gui.ROOT.after(500, lambda: mb.showinfo(
                    "Success",
                    f"Batch conversion completed successfully! Converted {successful_files} of {total_files} files.\nSaved to: {out_folder_path}"
                ))
            else:
                self.gui.ROOT.after(500, lambda: mb.showerror("Error", "Failed to convert any files."))

        except Exception as e:
            # Show error message
            self.gui.ROOT.after(500, lambda: mb.showerror("Error", f"An error occurred during batch conversion:\n{e}"))

        finally:
            # Hide loading screen
            self.gui.ROOT.after(100, self.gui.hide_loading_screen)
