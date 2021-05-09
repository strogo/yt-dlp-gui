import PySimpleGUI as sg
import os
import time
import re
sg.theme('SystemDefault')

def settings():
    layout = [
        [sg.Button("Download/Update yt-dlp", key="downloadytdlp")]
    ]
    window = sg.Window("Settings", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "downloadytdlp":
            os.system("curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -o yt-dlp.exe")

    window.close

def downloading():
    layout = [
        [sg.Text("The requested file is downloading...")],
        [sg.Text("How long the downloading takes depends on your internet speed")]
    ]
    window = sg.Window("Downloading...", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
       
    
    window.close()

def main():
    layout = [
        [sg.Text("Select format:")],
        [sg.Combo(["WebM", "MP4", "MP3", "M4A"], default_value="WebM", size=(6, 5))],
        [sg.Text('URL', size =(15, 1)), sg.InputText()],
        [sg.Button("Download", key="download")],
        [sg.Button("Settings", key="settings")]
    ]
    window = sg.Window("yt-dlp-gui", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "download":
            regex = re.match("https://www.youtube.com/watch?", values[1])
            if regex:
                sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                download(values)
            else:
                regex2 = re.search("^www.youtube.com/watch?", values[1])
                if regex2:
                    sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                    download(values)
                else:
                    regex3 = re.search("^https://youtube.com/watch?", values[1])
                    if regex3:
                        sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                        download(values)
                    else:
                        regex4 = re.search("^youtube.com/watch?", values[1])
                        if regex4:
                            sg.popup("The requested file is downloading... \nHow long the downloading takes depends on your internet speed", auto_close=True, auto_close_duration=5, keep_on_top=True)
                            download(values)
                        else:
                            sg.popup("Invalid URL", auto_close=True, auto_close_duration=5, keep_on_top=True)
            
            
            
        if event == "settings":
            settings()
        
    window.close()

def download(values):
    if values[0] == "WebM":
        os.system("yt-dlp.exe -f webm " + values[1])
    elif values[0] == "MP4":
        os.system("yt-dlp.exe -f mp4 " + values[1])
    elif values[0] == "MP3":
        os.system("yt-dlp.exe -x --audio-format mp3 " + values[1])
    elif values[0] == "M4A":
        os.system("yt-dlp.exe -x --audio-format m4a " + values[1])

if __name__ == "__main__":
    main()