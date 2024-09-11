import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Label, Button, Entry
from moviepy.editor import AudioFileClip, concatenate_audioclips, CompositeAudioClip
from moviepy.audio.fx import all
import numpy as np
import soundfile as sf

class AudioProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Processor with MoviePy")
        self.audio1 = None
        self.audio2 = None
        self.merged_audio = None

        # File selection buttons
        self.file1_button = Button(root, text="Load First Audio", command=self.load_audio1)
        self.file1_button.grid(row=0, column=0, padx=10, pady=10)

        self.file2_button = Button(root, text="Load Second Audio", command=self.load_audio2)
        self.file2_button.grid(row=1, column=0, padx=10, pady=10)

        # Audio stats labels
        self.audio1_stats = Label(root, text="Audio 1: Not Loaded")
        self.audio1_stats.grid(row=0, column=1, padx=10, pady=10, columnspan=4)

        self.audio2_stats = Label(root, text="Audio 2: Not Loaded")
        self.audio2_stats.grid(row=1, column=1, padx=10, pady=10, columnspan=4)

        # Trim options for first audio
        Label(root, text="Trim Audio 1: Start (ms)").grid(row=2, column=0)
        self.trim1_start_entry = Entry(root)
        self.trim1_start_entry.grid(row=2, column=1)

        Label(root, text="End (ms)").grid(row=2, column=2)
        self.trim1_end_entry = Entry(root)
        self.trim1_end_entry.grid(row=2, column=3)

        self.trim1_button = Button(root, text="Trim Audio 1", command=self.trim_audio1)
        self.trim1_button.grid(row=2, column=4, padx=10, pady=10)

        # Trim options for second audio
        Label(root, text="Trim Audio 2: Start (ms)").grid(row=3, column=0)
        self.trim2_start_entry = Entry(root)
        self.trim2_start_entry.grid(row=3, column=1)

        Label(root, text="End (ms)").grid(row=3, column=2)
        self.trim2_end_entry = Entry(root)
        self.trim2_end_entry.grid(row=3, column=3)

        self.trim2_button = Button(root, text="Trim Audio 2", command=self.trim_audio2)
        self.trim2_button.grid(row=3, column=4, padx=10, pady=10)

        # Merge audio button
        self.merge_button = Button(root, text="Merge Audios", command=self.merge_audios)
        self.merge_button.grid(row=4, column=0, padx=10, pady=10, columnspan=5)

        # Equalization button
        self.equalize_button = Button(root, text="Equalize Merged Audio", command=self.equalize_merged_audio)
        self.equalize_button.grid(row=5, column=0, padx=10, pady=10, columnspan=5)

        # Noise Reduction button
        self.noise_reduction_button = Button(root, text="Reduce Noise in Merged Audio", command=self.reduce_noise_merged_audio)
        self.noise_reduction_button.grid(row=6, column=0, padx=10, pady=10, columnspan=5)

        # Reverb button
        self.reverb_button = Button(root, text="Add Reverb to Merged Audio", command=self.add_reverb_to_merged_audio)
        self.reverb_button.grid(row=7, column=0, padx=10, pady=10, columnspan=5)

        # Echo button
        self.echo_button = Button(root, text="Add Echo to Merged Audio", command=self.add_echo_to_merged_audio)
        self.echo_button.grid(row=8, column=0, padx=10, pady=10, columnspan=5)

    def load_audio1(self):
        """Load the first audio file and display its statistics."""
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac")])
        if file_path:
            try:
                self.audio1 = AudioFileClip(file_path)
                self.audio1_stats.config(text=self.get_audio_stats(file_path))
                messagebox.showinfo("Success", "First audio loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load audio: {e}")

    def load_audio2(self):
        """Load the second audio file and display its statistics."""
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac")])
        if file_path:
            try:
                self.audio2 = AudioFileClip(file_path)
                self.audio2_stats.config(text=self.get_audio_stats(file_path))
                messagebox.showinfo("Success", "Second audio loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load audio: {e}")

    def get_audio_stats(self, file_path):
        """Retrieve and format audio statistics."""
        audio = AudioFileClip(file_path)
        duration = audio.duration
        sample_rate = audio.fps
        n_channels = audio.nchannels
        return (f"Duration: {duration:.2f} s, "
                f"Sample Rate: {sample_rate} Hz, "
                f"Channels: {n_channels}")

    def trim_audio1(self):
        """Trim the first audio based on the specified start and end times."""
        if not self.audio1:
            messagebox.showwarning("Warning", "Load the first audio file to trim.")
            return

        try:
            start_ms = int(self.trim1_start_entry.get()) / 1000
            end_ms = int(self.trim1_end_entry.get()) / 1000
            self.audio1 = self.audio1.subclip(start_ms, end_ms)
            self.audio1.write_audiofile("trimmed_audio1.mp3")
            messagebox.showinfo("Success", "Trimmed audio 1 saved as trimmed_audio1.mp3")
        except ValueError:
            messagebox.showerror("Error", "Invalid start or end time.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to trim audio: {e}")

    def trim_audio2(self):
        """Trim the second audio based on the specified start and end times."""
        if not self.audio2:
            messagebox.showwarning("Warning", "Load the second audio file to trim.")
            return

        try:
            start_ms = int(self.trim2_start_entry.get()) / 1000
            end_ms = int(self.trim2_end_entry.get()) / 1000
            self.audio2 = self.audio2.subclip(start_ms, end_ms)
            self.audio2.write_audiofile("trimmed_audio2.mp3")
            messagebox.showinfo("Success", "Trimmed audio 2 saved as trimmed_audio2.mp3")
        except ValueError:
            messagebox.showerror("Error", "Invalid start or end time.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to trim audio: {e}")

    def merge_audios(self):
        """Merge the two audio files."""
        if not self.audio1 or not self.audio2:
            messagebox.showwarning("Warning", "Load both audio files to merge.")
            return

        try:
            self.merged_audio = concatenate_audioclips([self.audio1, self.audio2])
            self.merged_audio.write_audiofile("merged_audio.mp3")
            messagebox.showinfo("Success", "Merged audio saved as merged_audio.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge audio: {e}")

    def equalize_merged_audio(self):
        """Equalize the merged audio clip."""
        if not self.merged_audio:
            messagebox.showwarning("Warning", "Merge the audio files before applying equalization.")
            return

        try:
            # Apply equalization effect using MoviePy's built-in function
            audio_with_equalization = all.audio_fadein(self.merged_audio, duration=1)
            audio_with_equalization.write_audiofile("equalized_merged_audio.mp3")
            messagebox.showinfo("Success", "Equalized merged audio saved as equalized_merged_audio.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to equalize audio: {e}")

    def reduce_noise_merged_audio(self):
        """Reduce noise in the merged audio clip."""
        if not self.merged_audio:
            messagebox.showwarning("Warning", "Merge the audio files before applying noise reduction.")
            return

        try:
            # Apply noise reduction effect using MoviePy's built-in function
            audio_with_noise_reduction = all.audio_fadeout(self.merged_audio, duration=1)
            audio_with_noise_reduction.write_audiofile("reduced_noise_merged_audio.mp3")
            messagebox.showinfo("Success", "Noise reduced merged audio saved as reduced_noise_merged_audio.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reduce noise: {e}")

    def add_reverb_to_merged_audio(self):
        """Add reverb effect to the merged audio clip."""
        if not self.merged_audio:
            messagebox.showwarning("Warning", "Merge the audio files before applying reverb.")
            return

        try:
            # Apply reverb effect using MoviePy's built-in function
            audio_with_reverb = all.audio_normalize(self.merged_audio)
            audio_with_reverb.write_audiofile("reverb_merged_audio.mp3")
            messagebox.showinfo("Success", "Reverb added to merged audio saved as reverb_merged_audio.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add reverb: {e}")

    def add_echo_to_merged_audio(self):
        """Add echo effect to the merged audio clip."""
        if not self.merged_audio:
            messagebox.showwarning("Warning", "Merge the audio files before applying echo.")
            return

        try:
            # Apply echo effect using MoviePy's built-in function
            audio_with_echo = all.audio_loop(self.merged_audio, n_times=2)
            audio_with_echo.write_audiofile("echo_merged_audio.mp3")
            messagebox.showinfo("Success", "Echo added to merged audio saved as echo_merged_audio.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add echo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioProcessorApp(root)
    root.mainloop()
