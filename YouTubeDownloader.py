from pytube import YouTube
from pytube import Playlist
import os
import sys
from tkinter import messagebox
from tkinter import * 
import tkinter as tk
from PIL import ImageTk, Image
import moviepy.editor as mp
import re
from moviepy import *
from moviepy.editor import VideoFileClip
import webbrowser

import shutil

# Funktionen zum Herunterladen
def download_start(): 
    download_link = download_entry.get()
    if download_link == "":
        messagebox.showinfo('ERROR','Bitte füllen Sie das Feld aus!')
    else:
        yt = YouTube(download_link)
        root.title('Downloading...')
        video = yt.streams.get_highest_resolution()
        video.download('YouTube_Downloader_Projekt\Downloads\MP4')
        root.title('Download Complete! Download Another File...')
        download_entry.delete(0, END)
        

def download_mp3(): 
    download_mp3 = download_entry.get()
    if download_mp3 == "":
        messagebox.showinfo('ERROR','Bitte füllen Sie das Feld aus!')
    else:
        yt = YouTube(download_mp3)
        root.title('Downloading...')
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download('YouTube_Downloader_Projekt\Downloads\MP3')
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        root.title('Download Complete! Download Another File...')
        download_entry.delete(0, END)

def download_playlist(): 
    download_playlist = download_entry.get()
    if download_playlist == "":
        messagebox.showinfo('ERROR','Bitte füllen Sie das Feld aus!')
    else:
        p = Playlist(download_playlist)
        root.title('Downloading...')
        for video in p.videos:
            video.streams.get_highest_resolution().download('YouTube_Downloader_Projekt\Downloads\MP4\Playlist')
            root.title('Download Complete! Download Another File...')
            download_entry.delete(0, END)
            

def download_mp3playlist(): 
    download_mp3playlist = download_entry.get()
    if download_mp3playlist == "":
        messagebox.showinfo('ERROR','Bitte füllen Sie das Feld aus!')
    else:
        p = Playlist(download_mp3playlist)
        root.title('Downloading...')
        for video in p.videos:
            out_file = video.streams.filter(only_audio=True).first().download('YouTube_Downloader_Projekt\Downloads\MP3\Playlist')
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            root.title('Download Complete! Download Another File...')
            download_entry.delete(0, END)

# Funktion zum Neustart des Programms
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# GUI-Setup
root = tk.Tk()
root.title("Youtube Downloader [Vollversion 2.0 German]")
root.iconbitmap('iconmain.ico')
root.geometry("853x638")
root.resizable(width=0, height=0)
root.config(bg="#1f1f1f")
img = PhotoImage(file="yt_background.png")
label = Label(
    root,
    image=img
)
label.place(x=0, y=0)
# Paste-
paste_button = Button(root, text="Einfügen", command=lambda:download_entry.event_generate("<<Paste>>"), bg="#ff0000", fg="white", font=("Helvetica", 14))
paste_button.place(x=660, y=204)

#Download-Buttons
mp4_button = Button(root, text="MP4 Download", command=download_start, bg="#ff0000", fg="white", font=("", 14))
mp4_button.place(relx=0.5, rely=0.5, anchor='center')
mp3_button = Button(root, text="MP3 Download", command=download_mp3, bg="#ff0000", fg="white", font=("", 14))
mp3_button.place(relx=0.5, rely=0.6, anchor='center')
playlist_button = Button(root, text="MP4 Playlist Download", command=download_playlist, bg="#ff0000", fg="white", font=("Helvetica", 14))
playlist_button.place(relx=0.5, rely=0.7, anchor='center')
playlistmp3_button = Button(root, text="MP3 Playlist Download", command=download_mp3playlist, bg="#ff0000", fg="white", font=("Helvetica", 14))
playlistmp3_button.place(relx=0.5, rely=0.8, anchor='center')

#Eingabefeld und Label
download_label = tk.Label(root, text="Kopiere deinen gewünschten YouTube hier hin:", bg="#2A2A2A", fg="white", font=("Helvetica", 14))
download_label.place(relx=0.5, rely=0.3, anchor='center')
download_entry = Entry(root, bd=5, width=40, bg="#adafad", fg="#000000", font=("Helvetica", 14))
download_entry.place(relx=0.5,rely=0.350, anchor='center')


# Info-Label
info_label = tk.Label(root, text="Die höchste Qualität beträgt HD (720p)", bg="#2A2A2A", fg="red", font=("Helvetica", 12))
info_label.place(x=377, y=240)

# Footer
footer_label = tk.Label(root, text="© 2023 YouTube Downloader. Alle Rechte vorbehalten.", bg="#2A2A2A", fg="white", font=("Helvetica", 10))
footer_label.place(x=0, y=615)

footer_label = tk.Label(root, text="➱Vollversion 2.0", bg="#2A2A2A", fg="white", font=("Helvetica", 10))
footer_label.place(x=0, y=592)


# Restart-Button
restart_button = Button(root, text="Exit Programm", command=exit, bg="#ff0000", fg="white", font=("Helvetica", 14))
restart_button.place(x=712, y=600)


#Website
def open_website():
    webbrowser.open_new("https://jdlpixel.de/download")

#Contact
def open_contact():
    webbrowser.open_new("https://github.com/JDLPIXEL")

button = Button(root, text="Website", command=open_website, bg="#ff0000", fg="white", font=("Helvetica", 14))
button.pack()
button.place(x=625, y=600)

button = Button(root, text="Contact", command=open_contact, bg="#ff0000", fg="white", font=("Helvetica", 14))
button.pack()
button.place(x=543, y=600)

root.mainloop()


root.mainloop()