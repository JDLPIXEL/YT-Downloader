from pytube import YouTube
from pytube import Playlist
import os
import sys
from tkinter import messagebox
from tkinter import * 
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Tk, Label, Button
import moviepy.editor as mp
import re
from moviepy import *
from moviepy.editor import VideoFileClip

import shutil

root = tk.Tk()
root.title("Youtube Downloader [Vollversion 1.0 German]")
root.iconbitmap(r'iconmain.ico')
root.geometry("853x638")
root.resizable(width=0, height=0)
root.config(bg="#1f1f1f")



img = PhotoImage(file="yt_background.png")
label = Label(
    root,
    image=img
)
label.place(x=0, y=500)

first_name = tk.Label(root, text="Kopiere deinen gewünschten YouTube Link hier hin: ", bg="#2A2A2A", fg="white")
first_name.place(x=270.33, y=130)

third_name = tk.Label(root, text="Die höchste Qualität beträgt HD (720p)", bg="#2A2A2A", fg="red")
third_name.place(x=0, y=420)

info_name = tk.Label(root, text="Infos \n ------------------------------------------------------------ \n - Falls der Download nicht funktioniert, kann es daran liegen das der Link inkorrekt ist. \n - Wichig! Es wird immer die Bestmögliche Downloadqualität beansprucht. \n - Fragen oder Fehlermeldung bitte an jdlpixel@gmail.com", bg="#2A2A2A", fg="red")
info_name.place(x=0, y=400)

last_name_entry = Entry(root, bd=5, width=40, bg="#adafad", fg="#000000")
last_name_entry.place(x=284.33, y=150)

def download_start(): 
    download_link = last_name_entry.get()
    if download_link == "":
        messagebox.showinfo('ERROR','Bitte füllen Sie das Feld aus!')
    else:
        yt = YouTube(download_link)
        root.title('Downloading...')
        video = yt.streams.get_highest_resolution()
        video.download('YouTube_Downloader_Projekt\Downloads\MP4')
        root.title('Download Complete! Download Another File...')
        last_name_entry.delete(0, END)
        

def download_mp3(): 
    download_mp3 = last_name_entry.get()
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
        last_name_entry.delete(0, END)

def download_playlist(): 
    download_playlist = last_name_entry.get()
    if download_playlist == "":
        messagebox.showinfo('ERROR','Bitte füllen Sie das Feld aus!')
    else:
        p = Playlist(download_playlist)
        root.title('Downloading...')
        for video in p.videos:
            video.streams.get_highest_resolution().download('YouTube_Downloader_Projekt\Downloads\MP4\Playlist')
            root.title('Download Complete! Download Another File...')
            last_name_entry.delete(0, END)
            

def download_mp3playlist(): 
    download_mp3playlist = last_name_entry.get()
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
            last_name_entry.delete(0, END)
           



confirm_button = Button(root, text="MP4 Download", command=download_start)
confirm_button.place(x=356.33, y=220)

mp3_button = Button(root, text="MP3 Download", command=download_mp3)
mp3_button.place(x=356.33, y=250)

playlist_button = Button(root, text="MP4 Playlist Download", command=download_playlist)
playlist_button.place(x=335.33, y=280)

playlistmp3_button = Button(root, text="MP3 Playlist Download", command=download_mp3playlist)
playlistmp3_button.place(x=335.33, y=310)

paste=tk.Button(root,text='Einfügen',
	command=lambda:last_name_entry.event_generate("<<Paste>>"),font=20,bg='cyan')
paste.place(x=365.33, y=180)
    
def restart():
    root.destroy()
    os.startfile("YouTube_Downloader.exe")


c_button = Button(root, text="Restart Programm", command=restart)
c_button.place(x=740, y=605)






root.mainloop()