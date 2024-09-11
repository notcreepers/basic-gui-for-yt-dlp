import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk
import pywinstyles
import sys
import os
import subprocess

# find out where icon is
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# find out where our resources are
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

yt_dlp_path = get_resource_path('resources/yt-dlp.exe')
ffmpeg_path = get_resource_path('resources/ffmpeg.exe')

# title bar theme
def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

# backend start

# ask user for file location
def choose_location():
    folder_selected = filedialog.askdirectory()
    save_location.set(folder_selected)

# fuck webm function
def check_format(url):
    command = [yt_dlp_path, '-F', url]
    result = subprocess.run(command, capture_output=True, text=True)
    formats = result.stdout
    format_lines = formats.splitlines()

    available_formats = {
        'webm': any('webm' in line for line in format_lines),
        'mp4': any('mp4' in line for line in format_lines)
    }

    return available_formats
    

# figure out the formats we have
def get_available_formats(url):
    command = [yt_dlp_path, '--list-formats', url]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# download the video
def download_video():
    url = youtube_url.get()
    location = save_location.get()
    quality = video_quality.get()
    audio_format = audio_format_var.get()
    download_audio = audio_only_var.get()

    if not url or not location:
        messagebox.showerror("Error", "Invalid link or save location.")
        return
    if download_audio:
        # go audio only mode
        command = [
            yt_dlp_path,
            '--extract-audio',
            '--audio-format', audio_format,
            url,
            '-o', f'{location}/%(title)s.%(ext)s'
        ]
           

        try:
            print(f"Executing command: {' '.join(command)}")
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Audio downloaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed.")
        return
    try:
        formats = check_format(url)
        print("Available formats:\n", formats)
    except Exception as e:
        messagebox.showerror("Error", f"Format check failed: {e}")
        return    
        
    if quality == 'best':
        command = [
            yt_dlp_path,
            '-f', 'bestvideo+bestaudio/best',
            '--remux-video', 'mp4',
            url,
            '-o', f'{location}/%(title)s.%(ext)s'
        ]
    elif formats['webm'] and not formats['mp4']:
        # ask if we want mp4
        if messagebox.askyesno("Remux to MP4", "The quality selected is only available in WEBM. Most applications do not have support for WEBM files. Do you want to convert it to MP4 automatically?"):
            command = [
                yt_dlp_path,
                '-f', quality,
                '--remux-video', 'mp4',
                url,
                '-o', f'{location}/%(title)s.%(ext)s'
            ]
        else:
            command = [
                yt_dlp_path,
                '-f', quality,
                url,
                '-o', f'{location}/%(title)s.%(ext)s'
            ]
    else:
        # mp4 is already available
        command = [
        yt_dlp_path,
        '-f', quality,
        url,
        '-o', f'{location}/%(title)s.%(ext)s'
    ]
        
        
    try:
        print(f"Executing command: {' '.join(command)}")
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Video downloaded.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Download failed.")

# backend end

# gui start

# main window
root = tk.Tk()
root.title("yt-dlp GUI")

# graphic design is my passion
icon_path = os.path.join(base_path, 'yt-dlp-gui-icon.ico')
root.iconbitmap(icon_path)

# link window
ttk.Label(root, text="Video URL:").pack(pady=5)
youtube_url = ttk.Entry(root, width=50)
youtube_url.pack(pady=5)

# save location window
ttk.Label(root, text="Save Location:").pack(pady=5)
save_location = tk.StringVar()
ttk.Entry(root, textvariable=save_location, width=50).pack(pady=5)
ttk.Button(root, text="Browse..", command=choose_location).pack(pady=5)

# select quality
ttk.Label(root, text="Video Quality:").pack(pady=5)
video_quality = tk.StringVar(value='best')
quality_options = ['best', 'worst', 'mp4', 'webm', 'flv']
ttk.OptionMenu(root, video_quality, *quality_options).pack(pady=5)

# audio only option
audio_only_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Download Audio", variable=audio_only_var).pack(pady=5)

# select audio format
ttk.Label(root, text="Audio Format:").pack(pady=5)
audio_format_var = tk.StringVar(value='mp3')
audio_format_options = ['mp3', 'm4a', 'opus', 'wav']
ttk.OptionMenu(root, audio_format_var, *audio_format_options).pack(pady=5)

# the button that does the magic
ttk.Button(root, text="Download", command=download_video).pack(pady=20)

# import theme
sv_ttk.set_theme("dark")

# title bar color
apply_theme_to_titlebar(root)

# run that ho
root.mainloop()