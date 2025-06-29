from tkinter import messagebox as mb
import Conversions as info
import os
import shutil
import subprocess
import threading
import time
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFont, ExifTags

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

    def resize_image_thread(self, file_path, output_folder, width, height, percentage, keep_aspect_ratio):
        """Handles image resizing in a separate thread to prevent UI freezing."""
        process_thread = threading.Thread(
            target=self._process_image_resize,
            args=(file_path, output_folder, width, height, percentage, keep_aspect_ratio)
        )
        process_thread.daemon = True
        self.gui.show_loading_screen() # You might want a more specific loading message
        process_thread.start()

    def _process_image_resize(self, file_path, output_folder, width, height, percentage, keep_aspect_ratio):
        """Actual image resizing logic."""
        try:
            img = Image.open(file_path)
            original_width, original_height = img.size

            if percentage:
                if not width and not height: # Only use percentage if specific dims aren't given
                    new_width = int(original_width * percentage / 100)
                    new_height = int(original_height * percentage / 100)
                else: # if specific dims are given with percentage, dims take precedence.
                      # This case should ideally be handled by input validation in controller
                    new_width = width if width else original_width
                    new_height = height if height else original_height
            elif width and height:
                new_width = width
                new_height = height
                if keep_aspect_ratio: # This might override one of the dimensions if both are provided
                    aspect_ratio = original_width / original_height
                    if new_width / new_height > aspect_ratio:
                        new_width = int(new_height * aspect_ratio)
                    else:
                        new_height = int(new_width / aspect_ratio)
            elif width: # Height is not provided
                new_width = width
                if keep_aspect_ratio:
                    new_height = int(original_height * new_width / original_width)
                else: # Use original height if not keeping aspect and height not provided
                    new_height = original_height
            elif height: # Width is not provided
                new_height = height
                if keep_aspect_ratio:
                    new_width = int(original_width * new_height / original_height)
                else: # Use original width if not keeping aspect and width not provided
                    new_width = original_width
            else:
                # Should not happen if controller validation is correct
                self.gui.ROOT.after(100, lambda: mb.showerror("Error", "No resize parameters specified."))
                return

            if new_width <= 0 or new_height <= 0:
                self.gui.ROOT.after(100, lambda: mb.showerror("Error", "Calculated dimensions are invalid (<=0)."))
                return

            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            # Preserve original extension, do not use a fixed 'resized' extension
            # Output filename like: originalname_resized.ext
            out_name = f"{name}_resized{ext}"
            out_path = os.path.join(output_folder, out_name)

            # Ensure unique filename
            increment = 0
            while os.path.exists(out_path):
                increment += 1
                out_name = f"{name}_resized_{increment}{ext}"
                out_path = os.path.join(output_folder, out_name)

            resized_img.save(out_path)
            img.close()
            resized_img.close()
            self.gui.ROOT.after(100, lambda: mb.showinfo("Success", f"Image resized successfully and saved to:\n{out_path}"))

        except FileNotFoundError:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", "Source image file not found."))
        except Exception as e:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", f"An error occurred during resizing:\n{e}"))
        finally:
            self.gui.ROOT.after(100, self.gui.hide_loading_screen)

    def compress_image_thread(self, file_path, output_folder, quality):
        """Handles image compression in a separate thread."""
        process_thread = threading.Thread(
            target=self._process_image_compression,
            args=(file_path, output_folder, quality)
        )
        process_thread.daemon = True
        self.gui.show_loading_screen() # Consider a "Compressing..." message
        process_thread.start()

    def _process_image_compression(self, file_path, output_folder, quality):
        """Actual image compression logic."""
        try:
            img = Image.open(file_path)
            original_format = img.format # Get original format to save in the same

            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)

            # Output filename like: originalname_compressed.ext
            out_name = f"{name}_compressed{ext}"
            out_path = os.path.join(output_folder, out_name)

            # Ensure unique filename
            increment = 0
            while os.path.exists(out_path):
                increment += 1
                out_name = f"{name}_compressed_{increment}{ext}"
                out_path = os.path.join(output_folder, out_name)

            save_options = {}
            if original_format in ['JPEG', 'WEBP']:
                save_options['quality'] = quality
            if original_format == 'PNG':
                save_options['optimize'] = True
                # Pillow's PNG compression level is 'compress_level' (0-9),
                # but 'optimize' is a good general approach.
                # For more control, one might map 'quality' to 'compress_level'.
                # Example: save_options['compress_level'] = 9 - (quality // 10) #粗略映射

            img.save(out_path, format=original_format, **save_options)
            img.close()

            original_size = os.path.getsize(file_path)
            compressed_size = os.path.getsize(out_path)
            reduction = original_size - compressed_size
            reduction_percent = (reduction / original_size) * 100 if original_size > 0 else 0

            success_message = (
                f"Image compressed successfully and saved to:\n{out_path}\n\n"
                f"Original size: {original_size / 1024:.2f} KB\n"
                f"Compressed size: {compressed_size / 1024:.2f} KB\n"
                f"Reduction: {reduction / 1024:.2f} KB ({reduction_percent:.2f}%)"
            )
            self.gui.ROOT.after(100, lambda: mb.showinfo("Success", success_message))

        except FileNotFoundError:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", "Source image file not found."))
        except Exception as e:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", f"An error occurred during compression:\n{e}"))
        finally:
            self.gui.ROOT.after(100, self.gui.hide_loading_screen)

    def adjust_color_thread(self, file_path, output_folder, brightness, contrast, saturation, selected_filter):
        """Handles color adjustment in a separate thread."""
        process_thread = threading.Thread(
            target=self._process_color_adjustment,
            args=(file_path, output_folder, brightness, contrast, saturation, selected_filter)
        )
        process_thread.daemon = True
        self.gui.show_loading_screen() # Consider an "Adjusting colors..." message
        process_thread.start()

    def _process_color_adjustment(self, file_path, output_folder, brightness_factor, contrast_factor, saturation_factor, selected_filter):
        """Actual color adjustment and filter logic."""
        try:
            img = Image.open(file_path)
            # Ensure image is in RGB mode for color adjustments, especially before applying Sepia
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')

            # Apply brightness
            if brightness_factor != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness_factor)

            # Apply contrast
            if contrast_factor != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast_factor)

            # Apply saturation (Color)
            if saturation_factor != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation_factor)

            # Apply filters
            if selected_filter == "Grayscale":
                img = ImageOps.grayscale(img)
                 # If original was RGBA and grayscale is applied, it becomes L mode.
                # To save as PNG with transparency, it might need converting back to LA or RGBA.
                # For simplicity, we'll let it save in the mode Pillow chooses after grayscale.
            elif selected_filter == "Sepia":
                img = self.apply_sepia_filter(img) # Custom function for sepia

            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)

            # Determine suffix based on applied changes
            suffix_parts = []
            if brightness_factor != 1.0: suffix_parts.append("b")
            if contrast_factor != 1.0: suffix_parts.append("c")
            if saturation_factor != 1.0: suffix_parts.append("s")
            if selected_filter != "None": suffix_parts.append(selected_filter.lower())

            suffix_str = "_adjusted"
            if suffix_parts:
                suffix_str = "_" + "".join(suffix_parts)

            out_name = f"{name}{suffix_str}{ext}"
            out_path = os.path.join(output_folder, out_name)

            increment = 0
            while os.path.exists(out_path):
                increment += 1
                out_name = f"{name}{suffix_str}_{increment}{ext}"
                out_path = os.path.join(output_folder, out_name)

            img.save(out_path) # Pillow will try to save in original format if not specified
            img.close()

            self.gui.ROOT.after(100, lambda: mb.showinfo("Success", f"Image adjustments applied and saved to:\n{out_path}"))

        except FileNotFoundError:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", "Source image file not found."))
        except Exception as e:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", f"An error occurred during color adjustment:\n{e}"))
        finally:
            self.gui.ROOT.after(100, self.gui.hide_loading_screen)

    def apply_sepia_filter(self, img):
        """Applies a sepia filter to an image."""
        if img.mode != 'RGB':
            img = img.convert('RGB')

        width, height = img.size
        pixels = img.load()

        for py in range(height):
            for px in range(width):
                r, g, b = img.getpixel((px, py))

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                pixels[px, py] = (min(255,tr), min(255,tg), min(255,tb))
        return img

    def apply_watermark_thread(self, base_image_path, output_folder, watermark_type,
                               text_content, font_size, # text_color,
                               watermark_image_path, opacity, position):
        """Handles watermark application in a separate thread."""
        process_thread = threading.Thread(
            target=self._process_watermark_application,
            args=(base_image_path, output_folder, watermark_type,
                  text_content, font_size, # text_color,
                  watermark_image_path, opacity, position)
        )
        process_thread.daemon = True
        self.gui.show_loading_screen()
        process_thread.start()

    def _process_watermark_application(self, base_image_path, output_folder, watermark_type,
                                       text_content, font_size, # text_color,
                                       watermark_image_path, opacity, position):
        """Actual watermark application logic."""
        try:
            base_img = Image.open(base_image_path).convert("RGBA")
            txt_layer = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            watermark_width, watermark_height = 0, 0

            if watermark_type == "Text":
                try:
                    # Attempt to load a default font. System-dependent.
                    # For more robust font handling, provide a font file with the app or allow user selection.
                    font = ImageFont.truetype("arial.ttf", int(font_size))
                except IOError:
                    font = ImageFont.load_default() # Fallback to a basic default font
                    mb.showwarning("Font Error", "Arial font not found. Using default system font. Size may vary.")


                # Get text size using textbbox for better accuracy
                bbox = draw.textbbox((0,0), text_content, font=font)
                watermark_width = bbox[2] - bbox[0]
                watermark_height = bbox[3] - bbox[1]

                # Text color: For simplicity, using white with controllable opacity via the alpha channel of txt_layer
                text_fill_color = (255, 255, 255, int(255 * opacity)) # White, with opacity

            elif watermark_type == "Image":
                watermark_img_original = Image.open(watermark_image_path).convert("RGBA")

                # Adjust opacity of watermark image
                if opacity < 1.0:
                    alpha = watermark_img_original.split()[3]
                    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                    watermark_img_original.putalpha(alpha)

                watermark_width, watermark_height = watermark_img_original.size
                # For image watermarks, we'll paste directly onto base_img later if not tiling
                # If tiling, we'll paste onto txt_layer first.

            # Calculate positions
            margin = 10
            positions = {
                "top-left": (margin, margin),
                "top-right": (base_img.width - watermark_width - margin, margin),
                "bottom-left": (margin, base_img.height - watermark_height - margin),
                "bottom-right": (base_img.width - watermark_width - margin, base_img.height - watermark_height - margin),
                "center": ((base_img.width - watermark_width) // 2, (base_img.height - watermark_height) // 2),
            }

            if position == "tile":
                for y in range(0, base_img.height, watermark_height + margin*5): # margin*5 for spacing between tiles
                    for x in range(0, base_img.width, watermark_width + margin*5):
                        if watermark_type == "Text":
                            draw.text((x, y), text_content, font=font, fill=text_fill_color)
                        elif watermark_type == "Image":
                            txt_layer.paste(watermark_img_original, (x,y), watermark_img_original) # Paste with alpha
            else:
                pos_x, pos_y = positions.get(position, positions["center"])
                if watermark_type == "Text":
                    draw.text((pos_x, pos_y), text_content, font=font, fill=text_fill_color)
                elif watermark_type == "Image":
                    # For single image watermark, paste directly onto a copy of base_img or use txt_layer
                    # Using txt_layer to keep the compositing step consistent
                    txt_layer.paste(watermark_img_original, (pos_x, pos_y), watermark_img_original)


            out_img = Image.alpha_composite(base_img, txt_layer)
            # Convert back to RGB if original didn't have alpha, to save as JPG etc.
            # However, if opacity < 1, RGBA is needed. Let Pillow handle format on save.
            # if base_img.mode == 'RGB' and out_img.mode == 'RGBA':
            #    out_img = out_img.convert('RGB')


            base_name_orig = os.path.basename(base_image_path)
            name, ext = os.path.splitext(base_name_orig)
            out_name = f"{name}_watermarked{ext}"
            out_path = os.path.join(output_folder, out_name)

            increment = 0
            while os.path.exists(out_path):
                increment += 1
                out_name = f"{name}_watermarked_{increment}{ext}"
                out_path = os.path.join(output_folder, out_name)

            out_img.save(out_path)
            base_img.close()
            txt_layer.close()
            out_img.close()
            if watermark_type == "Image" and 'watermark_img_original' in locals():
                watermark_img_original.close()

            self.gui.ROOT.after(100, lambda: mb.showinfo("Success", f"Watermark applied and saved to:\n{out_path}"))

        except FileNotFoundError:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", "One or more image files not found."))
        except Exception as e:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", f"An error occurred during watermarking:\n{e}"))
        finally:
            self.gui.ROOT.after(100, self.gui.hide_loading_screen)


    def read_metadata(self, file_path):
        """Reads EXIF metadata from an image file."""
        try:
            img = Image.open(file_path)
            exif_data_raw = img.getexif()
            img.close()

            if not exif_data_raw:
                mb.showinfo("Metadata", "No EXIF metadata found in this image.")
                return {}

            exif_data_readable = {}
            # These are the specific tags we are interested in for editing
            # Pillow stores them with integer keys. We need their string names.
            # Common string tags: Artist (315), Copyright (33432), ImageDescription (270)
            tag_map = {
                315: "Artist",
                33432: "Copyright",
                270: "ImageDescription"
                # Add other simple string tags here if desired
            }

            for k, v in exif_data_raw.items():
                tag_name = ExifTags.TAGS.get(k, k) # Get readable name if available
                if k in tag_map: # If it's one of our target tags
                    exif_data_readable[tag_map[k]] = v if isinstance(v, str) else str(v)
                # For general viewing (if a text box was used):
                # elif isinstance(v, bytes):
                #     exif_data_readable[tag_name] = v.decode(errors='replace') # Decode bytes if possible
                # else:
                #     exif_data_readable[tag_name] = str(v)
            return exif_data_readable

        except FileNotFoundError:
            mb.showerror("Error", "Image file not found.")
            return None
        except Exception as e:
            mb.showerror("Error", f"Could not read metadata: {e}")
            return None

    def edit_metadata_thread(self, file_path, output_folder, metadata_dict):
        """Handles metadata editing in a separate thread."""
        process_thread = threading.Thread(
            target=self._process_metadata_edit,
            args=(file_path, output_folder, metadata_dict)
        )
        process_thread.daemon = True
        self.gui.show_loading_screen()
        process_thread.start()

    def _process_metadata_edit(self, file_path, output_folder, metadata_dict):
        """Actual metadata editing and saving logic."""
        try:
            img = Image.open(file_path)
            exif_dict = img.getexif() # Get existing EXIF data
            if exif_dict is None:
                exif_dict = {} # Create new exif dict if none exists

            # Map our human-readable names back to EXIF integer tags
            # Ensure these tags are supported for writing by Pillow/libtiff
            # Artist (315), Copyright (33432), ImageDescription (270)
            # These are IFD0 tags, generally safe.
            tag_to_id = {
                "Artist": 315,
                "Copyright": 33432,
                "ImageDescription": 270
            }

            for key, value in metadata_dict.items():
                tag_id = tag_to_id.get(key)
                if tag_id is not None:
                    if value: # Only add/update if value is not empty
                        exif_dict[tag_id] = value
                    elif tag_id in exif_dict: # Remove if value is empty and tag exists
                        del exif_dict[tag_id]

            # Pillow expects EXIF data as bytes for the save method's exif parameter
            try:
                exif_bytes = Image.Exif.dump(exif_dict)
            except Exception as e:
                 # If exif_dict is empty or contains incompatible data for dumping,
                 # Pillow might raise an error.
                 # In such cases, we might choose to save without exif or with an empty exif_bytes
                if not exif_dict: # If dict is empty, make exif_bytes empty as well
                    exif_bytes = b''
                else: # If there was an error dumping non-empty dict, log and proceed without exif
                    print(f"Could not dump EXIF data: {e}. Saving without EXIF.")
                    exif_bytes = b''


            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            out_name = f"{name}_meta_edited{ext}" # Save as new file
            out_path = os.path.join(output_folder, out_name)

            increment = 0
            while os.path.exists(out_path):
                increment += 1
                out_name = f"{name}_meta_edited_{increment}{ext}"
                out_path = os.path.join(output_folder, out_name)

            # Important: EXIF data is primarily supported for JPEG, TIFF.
            # PNG typically uses `pnginfo` parameter, not `exif`.
            # For simplicity, this example focuses on `exif` which works best for JPEG.
            if img.format in ["JPEG", "TIFF"]:
                img.save(out_path, exif=exif_bytes)
            else:
                # For other formats, save without attempting to write EXIF via 'exif' param.
                # PNG metadata would need `PngImagePlugin.PngInfo` object.
                img.save(out_path)
                mb.showwarning("Metadata Save", f"EXIF metadata saving is primarily for JPEG/TIFF. Image saved, but EXIF might not be updated for {img.format} format.")

            img.close()
            self.gui.ROOT.after(100, lambda: mb.showinfo("Success", f"Image with updated metadata saved to:\n{out_path}"))

        except FileNotFoundError:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", "Source image file not found."))
        except Exception as e:
            self.gui.ROOT.after(100, lambda: mb.showerror("Error", f"An error occurred while saving metadata:\n{e}"))
        finally:
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
