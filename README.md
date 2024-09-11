# basic-gui-for-yt-dlp
Fairly barebones GUI for yt-dlp

## Backstory
Got pretty bored one night and decided "Fuck it, let's make a GUI for yt-dlp in python." Not expecting much to come from this. My first main python project and potentially my last.

## Installation
Literally just download the exe and run it. If you don't feel comfortable doing that, check my code and build it yourself. I used pyinstaller so it's gonna get picked up as a trojan by a few AVs. If you're using Avast, that's your fault. Also I don't care enough to make the yt-dlp window actually hide itself, so don't soil yourself when the command prompt opens and closes.

## Build "Instructions"
Basically just throw the script into the same directory as yt-dlp and ffmpeg, and use pyinstaller. You'll need to install a few things, namely [pywinstyles](https://github.com/Akascape/py-window-styles) and [sv_ttk](https://github.com/rdbende/Sun-Valley-ttk-theme). Lastly you'll need the .ico file (or one of your own). The gui.spec file is mostly setup for you, all you have to do is add the file path for everything I've mentioned.

## Updates
Probably not going to update this very often unless I feel I need to fix something. Works well for my needs. I mainly set it up just for YouTube, so results may vary for other websites.

## VirusTotal
I already went ahead and ran it through VirusTotal myself. The sandboxes think it behaves like a crypto miner, neat.
https://www.virustotal.com/gui/file/38c4495b948241b265ca9a1306b18e4f8688332f80749e7f0d09a8fb0e348d01/behavior

## Other Fun Facts
Fun fact 1. There's a handful of code that doesn't do anything. Like finding out if the download is a WEBM so it can be remuxed. I didn't feel like fixing it so I just made it so if you download the best quality it'll just try to remux. If it's already MP4 it won't.

Fun fact 2. There's no point in putting my name like properly in the code or anything since this is open source and if someone really wanted to steal it they can just edit my name out of the code. So tbh I'll just ask that you don't.
