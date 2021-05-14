import PySimpleGUI as sg
import os
import time
import re
import requests
from json import (load as jsonload, dump as jsondump)
from os import path
import subprocess as sp
from subprocess import call
from pyunpack import Archive
import shutil
from threading import Thread
sg.theme('SystemDefault')

downloadsuser = "C:/Users/" + os.getlogin() + "/Downloads"
SETTINGS_FILE = path.join(path.dirname(__file__), r'settings.cfg')
DEFAULT_SETTINGS = {'download_path' : downloadsuser}
# "Map" from the settings dictionary keys to the window's element keys
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'download_path': '-DOWNLOAD PATH-'}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        #sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved', icon=r'yt-dlp-gui-256.ico')

def settings_window(settings):
    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))
    layout = [
        [sg.Button("Download/Update yt-dlp and FFmpeg", key="downloadytdlpffmpeg")],
        [TextLabel('Download Path'), sg.Input(key='-DOWNLOAD PATH-')],
        [sg.Button('Save', key='save'), sg.Button('Exit', key='exit')]
    ]
    window = sg.Window("Settings", layout, keep_on_top=True, finalize=True, icon=r'yt-dlp-gui-256.ico')
    
    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:   # update window with the values read from settings file
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')
            
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "downloadytdlpffmpeg":
            call("curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -o yt-dlp.exe", shell=True)
            shutil.rmtree('ffmpeg')
            call("curl -L https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z -o ffmpeg.7z", shell=True)
            Archive('ffmpeg.7z').extractall("")
            rget = requests.get("https://www.gyan.dev/ffmpeg/builds/release-version")
            rcontent = rget.content
            ffmpegver = rcontent.decode('UTF-8')
            os.rename("ffmpeg-" + ffmpegver + "-full_build", "ffmpeg")
            os.remove("ffmpeg.7z")
            
        if event == 'save':
            window.close()
            save_settings(SETTINGS_FILE, settings, values)
            
        if event == 'exit':
            window.close()

    window.close

def download(values, settings):
    currentdir = os.getcwd()
    if values[0] == "WebM":
        call("yt-dlp.exe -o " + settings['download_path'] + "/%(title)s-%(id)s.%(ext)s --ffmpeg-location " + currentdir + "/ffmpeg/bin -f bestvideo[ext=webm]+bestaudio " + values[1], shell=True)
    elif values[0] == "MP4":
        call("yt-dlp.exe -o " + settings['download_path'] + "/%(title)s-%(id)s.%(ext)s --ffmpeg-location " + currentdir + "/ffmpeg/bin -f bestvideo[ext=mp4]+bestaudio " + values[1], shell=True)
    elif values[0] == "MP3":
        call("yt-dlp.exe -o " + settings['download_path'] + "/%(title)s-%(id)s.%(ext)s --ffmpeg-location " + currentdir + "/ffmpeg/bin -x --audio-format mp3 " + values[1], shell=True)
    elif values[0] == "M4A":
        call("yt-dlp.exe -o " + settings['download_path'] + "/%(title)s-%(id)s.%(ext)s --ffmpeg-location " + currentdir + "/ffmpeg/bin -x --audio-format m4a " + values[1], shell=True)

def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    layout = [
        [sg.Text("Select format:")],
        [sg.Combo(["WebM", "MP4", "MP3", "M4A"], default_value="WebM", size=(6, 5))],
        [sg.Text('URL', size =(15, 1)), sg.InputText()],
        [sg.Button("Download", key="download")],
        [sg.Button("Settings", key="settings")]
    ]
    window = sg.Window("yt-dlp-gui", layout, icon=r'yt-dlp-gui-256.ico')
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "download":
            t1 = Thread(target=download, args=(values, settings))
            regex = re.match("https://www.youtube.com/watch?", values[1])
            if regex:
                t1.start()
                sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
            else:
                regex2 = re.match("www.youtube.com/watch?", values[1])
                if regex2:
                    t1.start()
                    sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                else:
                    regex3 = re.match("https://youtube.com/watch?", values[1])
                    if regex3:
                        t1.start()
                        sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                    else:
                        regex4 = re.match("youtube.com/watch?", values[1])
                        if regex4:
                            t1.start()
                            sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                        else:
                            regex5 = re.match("https://www.youtu.be", values[1])
                            if regex5:
                                t1.start()
                                sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                            else:
                                regex6 = re.match("www.youtu.be", values[1])
                                if regex6:
                                    t1.start()
                                    sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                                else:
                                    regex7 = re.match("https://youtu.be?", values[1])
                                    if regex7:
                                        t1.start()
                                        sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                                    else:
                                        regex8 = re.match("youtu.be", values[1])
                                        if regex8:
                                            t1.start()
                                            sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                                        else:
                                            sg.popup("Invalid URL", auto_close=True, auto_close_duration=5, keep_on_top=True)

            
            
        if event == "settings":
            settings_window(settings)
        
    window.close()

if __name__ == "__main__":
    main()
