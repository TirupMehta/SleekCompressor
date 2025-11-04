import customtkinter as ctk
import tkinter
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import sys # <-- IMPORT SYS MODULE

# --- Main Application Class (FINAL VERSION) ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("SleekCompressor")
        self.geometry("600x450")
        ctk.set_appearance_mode("dark")
        self.resizable(False, False)
        
        # --- Configure the main window grid ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1) # Center content horizontally

        # --- File Selection Section ---
        self.file_label = ctk.CTkLabel(self.main_frame, text="Select a Video to Compress", font=ctk.CTkFont(size=16, weight="bold"))
        self.file_label.grid(row=0, column=0, pady=(10, 5))
        
        self.select_button = ctk.CTkButton(self.main_frame, text="Browse for Video File...", command=self.select_file)
        self.select_button.grid(row=1, column=0, pady=5, ipady=5)

        self.file_path_label = ctk.CTkLabel(self.main_frame, text="No file selected", text_color="gray", wraplength=500)
        self.file_path_label.grid(row=2, column=0, pady=5)

        # --- Settings Section ---
        self.settings_label = ctk.CTkLabel(self.main_frame, text="Compression Quality", font=ctk.CTkFont(size=16, weight="bold"))
        self.settings_label.grid(row=3, column=0, pady=(20, 5))

        self.crf_slider = ctk.CTkSlider(self.main_frame, from_=18, to=30, number_of_steps=12, width=300, command=self.update_slider_label)
        self.crf_slider.set(24)
        self.crf_slider.grid(row=4, column=0, pady=10)
        
        self.slider_value_label = ctk.CTkLabel(self.main_frame, text="24 (Good Balance)")
        self.slider_value_label.grid(row=5, column=0)

        # --- Action Button ---
        self.compress_button = ctk.CTkButton(self.main_frame, text="Compress Video", state="disabled", command=self.start_compression_thread, font=ctk.CTkFont(size=14, weight="bold"))
        self.compress_button.grid(row=6, column=0, pady=(30, 10), ipady=10, ipadx=20)
        
        # --- Progress & Status Section (at the bottom) ---
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.grid(row=1, column=0, padx=20, pady=(0,10), sticky="ew")
        self.status_frame.grid_columnconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Status: Ready")
        self.status_label.grid(row=0, column=1, sticky="w")
        
        self.about_button = ctk.CTkButton(self.status_frame, text="About", width=60, command=self.show_about_window)
        self.about_button.grid(row=0, column=2, sticky="e")

        self.progress_bar = ctk.CTkProgressBar(self.status_frame, mode='indeterminate')
        
        # --- Class Variables ---
        self.input_file_path = ""

    # --- NEW FUNCTION TO FIND FFMPEG ---
    def get_ffmpeg_path(self):
        """Gets the correct path to ffmpeg, whether running as a script or as a bundled exe."""
        if hasattr(sys, '_MEIPASS'):
            # Running in a PyInstaller bundle
            return os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        # Running as a normal script
        return 'ffmpeg.exe'

    def select_file(self):
        self.input_file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=(("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*"))
        )
        if self.input_file_path:
            self.file_path_label.configure(text=os.path.basename(self.input_file_path))
            self.compress_button.configure(state="normal")
            self.status_label.configure(text="Status: Ready to compress")
        else:
            self.file_path_label.configure(text="No file selected", text_color="gray")
            self.compress_button.configure(state="disabled")

    def update_slider_label(self, value):
        crf = int(value)
        label_text = f"{crf}"
        if crf <= 20: label_text += " (Higher Quality)"
        elif crf <= 26: label_text += " (Good Balance)"
        else: label_text += " (Smaller Size)"
        self.slider_value_label.configure(text=label_text)

    def start_compression_thread(self):
        self.compress_button.configure(state="disabled")
        self.select_button.configure(state="disabled")
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=(0,5))
        self.progress_bar.start()
        self.status_label.configure(text="Status: Compressing... Please wait.")
        thread = threading.Thread(target=self.run_compression)
        thread.start()

    def run_compression(self):
        try:
            ffmpeg_path = self.get_ffmpeg_path() # <-- GET THE CORRECT PATH
            crf_value = int(self.crf_slider.get())
            path, filename = os.path.split(self.input_file_path)
            name, ext = os.path.splitext(filename)
            output_file_path = os.path.join(path, f"{name}_compressed.mp4")
            
            # --- UPDATED COMMAND USING THE FULL PATH ---
            command = [ffmpeg_path, '-i', self.input_file_path, '-vcodec', 'libx264', '-crf', str(crf_value), '-preset', 'fast', output_file_path, '-y']
            
            subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.after(0, self.compression_finished, True, output_file_path)

        except subprocess.CalledProcessError:
            self.after(0, self.compression_finished, False, "", "FFmpeg failed. The selected file might be corrupt or not a video file.")
        except Exception as e:
            self.after(0, self.compression_finished, False, "", str(e))

    def compression_finished(self, success, result_path="", error_message=""):
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.compress_button.configure(state="normal")
        self.select_button.configure(state="normal")

        if success:
            self.status_label.configure(text="Status: Compression successful!")
            messagebox.showinfo("Success", f"Video compressed successfully!\n\nSaved as: {result_path}")
        else:
            self.status_label.configure(text="Status: An error occurred.")
            messagebox.showerror("Error", f"An error occurred during compression:\n\n{error_message}")
            
    def show_about_window(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("About SleekCompressor")
        about_window.geometry("400x220")
        about_window.resizable(False, False)
        about_window.transient(self)

        about_label = ctk.CTkLabel(about_window, text="SleekCompressor", font=ctk.CTkFont(size=20, weight="bold"))
        about_label.pack(pady=(20, 10))
        
        version_label = ctk.CTkLabel(about_window, text="Version 1.1")
        version_label.pack()
        
        copyright_label = ctk.CTkLabel(about_window, text="Copyright © 2025 Tirup Mehta. All Rights Reserved.")
        copyright_label.pack(pady=20)

        ok_button = ctk.CTkButton(about_window, text="OK", command=about_window.destroy)
        ok_button.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()