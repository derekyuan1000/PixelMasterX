from tkinter import messagebox as mb
import os
from PIL import Image
import threading

# Separate import handling for rembg to avoid crashes
REMBG_AVAILABLE = False
try:
    import rembg
    REMBG_AVAILABLE = True
except ImportError:
    pass

class BackgroundRemover:
    def __init__(self, controller):
        self.controller = controller
        self.gui = None
        self.converter = None

    def set_gui(self, gui):
        self.gui = gui

    def set_converter(self, converter):
        self.converter = converter

    def remove_background(self, file_paths):
        """Remove the background from image files using rembg library"""
        if not REMBG_AVAILABLE:
            mb.showerror(
                "Required Package Missing",
                "Background removal requires the 'rembg' package. Please install it by running 'pip install rembg'."
            )
            return

        if not file_paths or len(file_paths) == 0:
            mb.showerror("No File Selected", "Please select an image file first.")
            return

        # Check which UI section called this method
        if hasattr(self.gui, 'bg_file_paths') and file_paths == self.gui.bg_file_paths:
            # Called from the dedicated background removal screen
            output_folder = self.gui.bg_output_folder.get()
        else:
            # Called from the conversion screen
            output_folder = self.gui.output_folder.get()

        if not output_folder:
            mb.showerror("No Output Folder", "Please select an output folder first.")
            return

        # Create a separate thread for background processing
        process_thread = threading.Thread(
            target=self._process_background_removal,
            args=(file_paths, output_folder)
        )
        process_thread.daemon = True  # Thread will exit when main program exits

        # Start the thread and show loading screen
        self.gui.show_loading_screen()
        process_thread.start()

    def _process_background_removal(self, file_paths, output_folder):
        """Process background removal in a separate thread"""
        try:
            # Use the imported rembg module
            total_files = len(file_paths)
            successful_files = 0

            for i, file_path in enumerate(file_paths):
                # Update progress indicator
                file_name = os.path.basename(file_path)
                self.gui.update_progress(i, total_files, f"Processing {file_name}...")

                # Check if the file is an image
                ext = os.path.splitext(file_path)[1].lstrip('.').upper()
                if not self.converter.is_image_format(ext):
                    continue

                try:
                    # Process the image with rembg
                    input_img = Image.open(file_path)

                    # Remove the background
                    output_img = rembg.remove(input_img)

                    # Save the output image with transparent background
                    base_name = os.path.basename(file_path)
                    base, ext = os.path.splitext(base_name)
                    # Save as PNG to preserve transparency
                    out_path = self.converter.check_file_name(file_path, increment=0, to_format="png", output_folder=output_folder)
                    output_img.save(out_path)
                    successful_files += 1

                except Exception as img_error:
                    # Log the error but continue processing other images
                    print(f"Error processing {file_name}: {img_error}")
                    continue

            # Update final progress
            self.gui.update_progress(total_files, total_files, f"Completed! Processed {successful_files} of {total_files} images.")

            # Show success message
            if successful_files > 0:
                # Use after() to schedule the messagebox to appear after GUI updates
                self.gui.ROOT.after(500, lambda: mb.showinfo("Success", f"Background removal completed successfully! Processed {successful_files} of {total_files} images."))
            else:
                self.gui.ROOT.after(500, lambda: mb.showerror("Error", "Failed to process any images."))

        except Exception as e:
            # Show error message
            self.gui.ROOT.after(500, lambda: mb.showerror("Error", f"An error occurred during background removal:\n{e}"))

        finally:
            # Hide loading screen
            self.gui.ROOT.after(100, self.gui.hide_loading_screen)
