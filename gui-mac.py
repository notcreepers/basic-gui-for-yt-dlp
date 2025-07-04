import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk
import sys
import os
import subprocess
import re
import json
from io import BytesIO
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

def save_settings(settings):
    try:
        with open(config_path, 'w') as config_file:
            json.dump(settings, config_file)
    except Exception as e:
        print(f"Error saving config file: {e}")

settings = load_settings()

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

yt_dlp_path = get_resource_path('resources/yt-dlp')
ffmpeg_path = get_resource_path('resources/ffmpeg')
creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
print(sys._MEIPASS)

def fetch_metadata(url):
    command = [yt_dlp_path, '-j', url]
    result = subprocess.run(command, capture_output=True, text=True, creationflags=creationflags)
    metadata = json.loads(result.stdout)
    return metadata

#def download_thumbnail(thumbnail_url):
 #   response = requests.get(thumbnail_url, stream=True)
  #  if response.status_code == 200:
   #     img = Image.open(BytesIO(response.content))
    #    img.thumbnail((200, 200))
     #   return ImageTk.PhotoImage(img)
   # else:
    #    return None

#def update_video_info(metadata):
    video_title.set(metadata['title'])
    thumbnail_image = download_thumbnail(metadata['thumbnail'])
    if thumbnail_image:
        thumbnail_label.config(image=thumbnail_image)
        thumbnail_label.image = thumbnail_image

def update_progress_bar(output, progress_bar):
    match = re.search(r'(\d+)%', output)
    if match:
        percent = int(match.group(1))
        progress_bar['value'] = percent
        root.update_idletasks()

def choose_location():
    folder_selected = filedialog.askdirectory()
    save_location.set(folder_selected)

def check_format(url):
    command = [yt_dlp_path, '-F', url]
    result = subprocess.run(command, capture_output=True, text=True, creationflags=creationflags)
    formats = result.stdout
    format_lines = formats.splitlines()

    available_formats = {
        'webm': any('webm' in line for line in format_lines),
        'mp4': any('mp4' in line for line in format_lines)
    }

    return available_formats

def get_available_formats(url):
    command = [yt_dlp_path, '--list-formats', url]
    result = subprocess.run(command, capture_output=True, text=True, creationflags=creationflags)
    return result.stdout

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
    
    progress_bar['value'] = 0
    root.update_idletasks()

    try:
        metadata = fetch_metadata(url)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch metadata: {e}")
        return
    threading.Thread(target=handle_video_download, args=(url, location, quality, audio_format, download_audio)).start()

def handle_video_download(url, location, quality, audio_format, download_audio):
    try:
        if download_audio:
            command = [
                yt_dlp_path,
                '--extract-audio',
                '--audio-format', audio_format,
                url,
                '--no-mtime',
                '--ffmpeg-location', os.path.dirname(ffmpeg_path),
                '-o', f'{location}/%(title)s.%(ext)s'
            ]
            try:
                subprocess.run(command, check=True, creationflags=creationflags)
                messagebox.showinfo("Success", "Audio downloaded.")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed.")
            return

        try:
            formats = check_format(url)
        except Exception as e:
            messagebox.showerror("Error", f"Format check failed: {e}")
            return    

        if quality == 'best':
            command = [
                yt_dlp_path,
                '-f', 'bestvideo+bestaudio/best',
                '--remux-video', 'mp4',
                url,
                '--no-mtime',
                '--ffmpeg-location', os.path.dirname(ffmpeg_path),
                '-o', f'{location}/%(title)s.%(ext)s'
            ]
        elif formats['webm'] and not formats['mp4']:
            if messagebox.askyesno("Remux to MP4", "The quality selected is only available in WEBM. Do you want to convert it to MP4 automatically?"):
                command = [
                    yt_dlp_path,
                    '-f', quality,
                    '--remux-video', 'mp4',
                    url,
                    '--no-mtime',
                    '--ffmpeg-location', os.path.dirname(ffmpeg_path),
                    '-o', f'{location}/%(title)s.%(ext)s'
                ]
            else:
                command = [
                    yt_dlp_path,
                    '-f', quality,
                    url,
                    '--no-mtime',
                    '--ffmpeg-location', os.path.dirname(ffmpeg_path),
                    '-o', f'{location}/%(title)s.%(ext)s'
                ]
        else:
            command = [
                yt_dlp_path,
                '-f', quality,
                url,
                '--no-mtime',
                '--ffmpeg-location', os.path.dirname(ffmpeg_path),
                '-o', f'{location}/%(title)s.%(ext)s'
            ]

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=creationflags) as process:
            for line in process.stdout:
                update_progress_bar(line, progress_bar)
        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# gui

root = tk.Tk()
root.title("yt-dlp GUI")
root.geometry("420x640")

# set icon (use png on mac)
icon_path = os.path.join(base_path, 'resources/yt-dlp-gui-icon.png')
icon_image = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon_image)

ttk.Label(root, text="Video URL:").pack(pady=5)
youtube_url = ttk.Entry(root, width=50)
youtube_url.pack(pady=5)

ttk.Label(root, text="Save Location:").pack(pady=5)
save_location = tk.StringVar(value=settings.get('save_location', ''))
ttk.Entry(root, textvariable=save_location, width=50).pack(pady=5)
ttk.Button(root, text="Browse..", command=choose_location).pack(pady=5)

ttk.Label(root, text="Video Quality:").pack(pady=5)
video_quality = tk.StringVar(value='best')
quality_options = ['best', 'best', 'worst', 'mp4', 'webm', 'flv']
ttk.OptionMenu(root, video_quality, *quality_options).pack(pady=5)

audio_only_var = tk.BooleanVar(value=False)
ttk.Checkbutton(root, text="Only Download Audio", variable=audio_only_var).pack(pady=5)

ttk.Label(root, text="Audio Format:").pack(pady=5)
audio_format_var = tk.StringVar(value='mp3')
audio_format_options = ['mp3', 'mp3', 'm4a', 'opus', 'wav']
ttk.OptionMenu(root, audio_format_var, *audio_format_options).pack(pady=5)

video_title = tk.StringVar()
ttk.Label(root, textvariable=video_title).pack(pady=5)

thumbnail_label = ttk.Label(root)
thumbnail_label.pack(pady=5)

progress_bar = tk.ttk.Progressbar(root, length=300, mode="determinate", maximum=100)
progress_bar.pack(pady=20)

def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.iconphoto(True, icon_image)
    about_window.geometry("540x340")

    logo_image = tk.PhotoImage(file=get_resource_path('resources/yt-dlp-gui-icon.png'))
    logo_label = ttk.Label(about_window, image=logo_image)
    logo_label.image = logo_image
    logo_label.pack(pady=10)

    ttk.Label(about_window, text="yt-dlp GUI").pack(pady=10)
    ttk.Label(about_window, text="v1.1").pack(pady=5)
    ttk.Label(about_window, text="Made by Creepers").pack(pady=5)
    ttk.Label(about_window, text="Wouldn't be possible without: sv_ttk (rdbende)").pack(pady=5)

    ttk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=20)

def open_settings_window():
    settings = load_settings()
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.iconphoto(True, icon_image)
    settings_window.geometry("540x340")

    ttk.Label(settings_window, text="Advanced Settings").pack(pady=10)

    ttk.Label(settings_window, text="Default Save Location:").pack(pady=5)
    save_location_var = tk.StringVar(value=settings.get('save_location', ''))
    ttk.Entry(settings_window, textvariable=save_location_var, width=50).pack(pady=5)
    ttk.Button(settings_window, text="Browse..", command=lambda: browse_save_location(save_location_var)).pack(pady=5)

    def browse_save_location(save_location_var):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            save_location_var.set(folder_selected)

    def save_advanced_settings(save_location, window):
        settings = {
            "save_location": save_location,
        }
        save_settings(settings)
        messagebox.showinfo("Settings", "Settings saved successfully.")
        window.destroy()

    settings = load_settings()
    save_location.set(settings.get('save_location', ''))

    ttk.Button(settings_window, text="Save", command=lambda: save_advanced_settings(
        save_location_var.get(),
        settings_window
    )).pack(pady=10)

    ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=20)
    ttk.Label(settings_window, text="Changes will be applied after restart (sorry).").pack(pady=5)

ttk.Button(root, text="About", command=open_about_window).pack(side="left", anchor="sw", padx=10, pady=10)
ttk.Button(root, text="Download", command=download_video).pack(side="right", anchor="se", padx=10, pady=10)
ttk.Button(root, text="Settings", command=open_settings_window).pack(side="bottom", padx=5, pady=10)

sv_ttk.set_theme("dark")

root.mainloop()
