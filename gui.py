import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk
import pywinstyles
import sys
import os
import subprocess
import json
import requests
from PIL import Image, ImageTk
import threading



# fallback settings
default_settings = {
    "save_location": "",
    "video_quality": "best",
    "audio_format": "mp3",
    "download_audio": False

}

# user config location
config_path = os.path.join(os.path.expanduser("~"), "yt-dlp-gui-config.json")

# load user config
def load_settings():
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            return default_settings
    else:
        return default_settings
    
# save user config
def save_settings(settings):
    try:
        with open(config_path, 'w') as config_file:
            json.dump(settings, config_file)
    except Exception as e:
        print(f"Error saving config file: {e}")

settings = load_settings()

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

# get video metadata
def fetch_metadata(url):
    command = [yt_dlp_path, '-j', url]
    result = subprocess.run(command, capture_output=True, text=True)
    metadata = json.loads(result.stdout)
    return metadata

# download and display thumbnail
def download_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url, stream=True)
    if response.status_code == 200:
        img_data = response.raw
        img = Image.open(img_data)
        img.thumbnail((200, 200))
        return ImageTk.PhotoImage(img)
    else:
        return None
    
# add the thumbnail to the ui
def update_video_info(metadata):
    video_title.set(metadata['title'])
    thumbnail_image = download_thumbnail(metadata['thumbnail'])
    if thumbnail_image:
        thumbnail_label.config(image=thumbnail_image)
        thumbnail_label.image = thumbnail_image

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
    settings = load_settings()
    url = youtube_url.get()
    location = save_location.get() or settings.get('save_location', '')
    quality = video_quality.get()
    audio_format = audio_format_var.get()
    download_audio = audio_only_var.get()

    if not url or not location:
        messagebox.showerror("Error", "Invalid link or save location.")
        return
    try:
        metadata = fetch_metadata(url)
        update_video_info(metadata)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch metadata: {e}")
        return
    threading.Thread(target=handle_video_download, args=(url, location, quality, audio_format, download_audio)).start()
# download video on another thread   
def handle_video_download(url, location, quality, audio_format, download_audio):
 try:    
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
 except Exception as e:
     messagebox.showerror("Error", f"Something went wrong: {e}")
# backend end

# gui start

# about window
def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.iconbitmap(icon_path)
    about_window.geometry("540x340")
    pywinstyles.apply_style(about_window, "dark" if sv_ttk.get_theme() == "dark" else "normal")

    logo_image = tk.PhotoImage(file=get_resource_path('resources/yt-dlp-gui-icon.png'))
    logo_label = ttk.Label(about_window, image=logo_image)
    logo_label.image = logo_image
    logo_label.pack(pady=10)

    ttk.Label(about_window, text="yt-dlp GUI").pack(pady=10)
    ttk.Label(about_window, text="v1.0.4").pack(pady=5)
    ttk.Label(about_window, text="Made by Creepers").pack(pady=5)
    ttk.Label(about_window, text="Wouldn't be possible without: pywinstyles (Akaspace) and sv_ttk (rdbende)").pack(pady=5)

    ttk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=20)

# settings window
def open_settings_window():
    settings = load_settings()
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.iconbitmap(icon_path)
    settings_window.geometry("540x340")
    pywinstyles.apply_style(settings_window, "dark" if sv_ttk.get_theme() == "dark" else "normal")

    
    ttk.Label(settings_window, text="Advanced Settings").pack(pady=10)

    # user save location
    ttk.Label(settings_window, text="Default Save Location:").pack(pady=5)
    save_location_var = tk.StringVar(value=settings.get('save_location', ''))
    ttk.Entry(settings_window, textvariable=save_location_var, width=50).pack(pady=5)
    ttk.Button(settings_window, text="Browse..", command=lambda: browse_save_location(save_location_var)).pack(pady=5)

    # save settings and close button
    ttk.Button(settings_window, text="Save", command=lambda: save_advanced_settings(
        save_location_var.get(),
        settings_window
    )).pack(pady=10)

    # browser for save location
    def browse_save_location(save_location_var):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            save_location_var.set(folder_selected)
    
    # save user settings and close the window
    def save_advanced_settings(save_location, window):
        settings = {
            "save_location": save_location,
        }
        save_settings(settings)
        
        messagebox.showerror("Settings", "Settings saved successfully.")
        window.destroy()
    
    # load user settings
    settings = load_settings()

    # set default
    save_location.set(settings.get('save_location', ''))

    ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=20)
    ttk.Label(settings_window, text="Changes will be applied after restart (sorry).").pack(pady=5)

# main window
root = tk.Tk()
root.title("yt-dlp GUI")
root.geometry("420x640")

# graphic design is my passion
icon_path = os.path.join(base_path, 'yt-dlp-gui-icon.ico')
root.iconbitmap(icon_path)

# link window
ttk.Label(root, text="Video URL:").pack(pady=5)
youtube_url = ttk.Entry(root, width=50)
youtube_url.pack(pady=5)

# save location window
ttk.Label(root, text="Save Location:").pack(pady=5)
save_location = tk.StringVar(value=settings.get('save_location', ''))
ttk.Entry(root, textvariable=save_location, width=50).pack(pady=5)
ttk.Button(root, text="Browse..", command=choose_location).pack(pady=5)

# select quality
ttk.Label(root, text="Video Quality:").pack(pady=5)
video_quality = tk.StringVar(value='best')
quality_options = ['best', 'best', 'worst', 'mp4', 'webm', 'flv']
ttk.OptionMenu(root, video_quality, *quality_options).pack(pady=5)

# audio only option
audio_only_var = tk.BooleanVar(value=False)
ttk.Checkbutton(root, text="Download Audio", variable=audio_only_var).pack(pady=5)

# select audio format
ttk.Label(root, text="Audio Format:").pack(pady=5)
audio_format_var = tk.StringVar(value='mp3')
audio_format_options = ['mp3', 'mp3', 'm4a', 'opus', 'wav']
ttk.OptionMenu(root, audio_format_var, *audio_format_options).pack(pady=5)

# title and thumbnail

video_title = tk.StringVar()
ttk.Label(root, textvariable=video_title).pack(pady=5)

thumbnail_label = ttk.Label(root)
thumbnail_label.pack(pady=5)

# about button
ttk.Button(root, text="About", command=open_about_window).pack(side="left", anchor="sw", padx=10, pady=10)

# the button that does the magic
ttk.Button(root, text="Download", command=download_video).pack(side="right", anchor="se", padx=10, pady=10)

# settings button
ttk.Button(root, text="Settings", command=open_settings_window).pack(side="bottom", padx=5, pady=10)

# import theme
sv_ttk.set_theme("dark")

# title bar color
apply_theme_to_titlebar(root)

# run that ho
root.mainloop()