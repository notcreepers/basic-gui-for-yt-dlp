# basic-gui-for-yt-dlp
Fairly barebones GUI for yt-dlp
## macOS Branch
This is the experimental macOS branch. Due to issues I had while attempting to compile for macOS, this version **CANNOT** display the thumbnail and title of the video currently downloading, or produce files that QuickTime will open (if you use best quality).
## Instructions
You **MUST** build this yourself. I cannot get a proper executable to work by itself.

Clone the repo. You need all the files except for README.md

You need the latest release of [python](https://www.python.org/downloads/macos/). From there use pip to install sv_ttk and pyinstaller.

Now download the latest releases of [yt-dlp](https://github.com/yt-dlp/yt-dlp/releases) and [FFmpeg](https://evermeet.cx/ffmpeg/). Put these in your "resources" folder.

Update gui-mac.spec to point to your directories. e.g. "/Users/*youruser*/Documents/VSC/basic-gui-for-yt-dlp/resources/ffmpeg". If you use the .spec file provided and copy my locations all you need to do is switch my username to yours. I was using Visual Studio Code so my python dependencies were in a .venv folder in the same basic-gui-for-yt-dlp folder. IF you do not want to use a virtual environment, point the dependencies to wherever your python packages are installed.

You can remove any references to PIL/Pillow. I realized they were not needed due to the removal of thumbnail and title fetching so they don't need to be in the file.

You should now be ready to put all this together. Open Terminal and navigate to the folder with gui-mac.spec and gui-mac.py. Now run "pyinstaller gui-mac.spec --clean". You *should* be able to just do this in the VSC terminal but I did not. If you do this in the macOS terminal you will need to use pip to install pyinstaller if you used a virtual environment.

Hopefully you don't have any errors. Once it's done head to the newly created "dist" folder and either open it in Terminal using "./gui-mac" or add the .app extension to it and double click it. It should ask for permission to access files in your Documents folder, allow it. It will then relaunch and you should see the GUI.

This was more of a proof of concept rather than a proper release so I will most likely not update it often. If you feel like fixing the issues with it or shit talking me, go ahead idgaf.

![yt-dlp-gui-icon](https://github.com/user-attachments/assets/c9cdc7ee-89d8-4fa0-9785-5ba4acbc5453)


