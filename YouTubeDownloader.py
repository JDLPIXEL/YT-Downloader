from pytube import YouTube
from pytube import Playlist
import os
import sys
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import threading
import tkinter.filedialog as filedialog
import webbrowser
import tkinter.scrolledtext as scrolledtext

# Funktion zum Anzeigen des Fehlerfensters
def show_error_window(error):
    # Erstelle ein neues Tkinter-Fenster
    error_window = tk.Toplevel()
    error_window.title("Fehler aufgetreten:")

    # ScrolledText-Widget zum Anzeigen des Fehlercodes
    text_widget = scrolledtext.ScrolledText(error_window, width=80, height=20, wrap=tk.WORD)
    text_widget.insert(tk.END, str(error))
    text_widget.pack(padx=10, pady=10)

    # Button zum Kopieren des Fehlercodes
    def copy_error():
        error_str = str(error)
        root.clipboard_clear()
        root.clipboard_append(error_str)
        root.update()

    copy_button = tk.Button(error_window, text="Fehlercode kopieren", command=copy_error)
    copy_button.pack(pady=10)

    # Button zum Melden von Fehlern auf Github
    def report_issue():
        webbrowser.open("https://github.com/JDLPIXEL/YT-Downloader/issues")

    report_issue_button = tk.Button(error_window, text="Fehler auf Github melden", command=report_issue)
    report_issue_button.pack(pady=10)

    # Hauptfenster deaktivieren, während das Fehlerfenster geöffnet ist
    error_window.transient(root)
    error_window.grab_set()
    root.wait_window(error_window)

# Funktion zum Herunterladen
def download_start():
    download_link = download_entry.get()
    folder_path = path_entry.get()  # Speicherpfad aus dem Textfeld abrufen
    if download_link == "":
        messagebox.showerror('ERROR', 'Bitte füllen Sie das Feld aus!')
    elif folder_path == "":
        messagebox.showerror('ERROR', 'Bitte geben Sie einen Speicherort an!')
    else:
        def download():
            try:
                yt = YouTube(download_link)
                root.title('Downloading...')
                video = yt.streams.get_highest_resolution()
                video.download(folder_path)
                root.title('Download Complete! Download Another File...')
                download_entry.delete(0, END)
            except Exception as e:
                show_error_window(e)

        # Download in einem separaten Thread ausführen
        thread = threading.Thread(target=download)
        thread.start()


def download_mp3():
    download_mp3 = download_entry.get()
    folder_path = path_entry.get()  # Speicherpfad aus dem Textfeld abrufen
    if download_mp3 == "":
        messagebox.showerror('ERROR', 'Bitte füllen Sie das Feld aus!')
    elif folder_path == "":
        messagebox.showerror('ERROR', 'Bitte geben Sie einen Speicherort an!')
    else:
        def download():
            try:
                yt = YouTube(download_mp3)
                root.title('Downloading...')
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(folder_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                root.title('Download Complete! Download Another File...')
                download_entry.delete(0, END)
            except Exception as e:
                show_error_window(e)

        # Download in einem separaten Thread ausführen
        thread = threading.Thread(target=download)
        thread.start()


def download_playlist():
    download_playlist = download_entry.get()
    folder_path = path_entry.get()  # Speicherpfad aus dem Textfeld abrufen
    if download_playlist == "":
        messagebox.showerror('ERROR', 'Bitte füllen Sie das Feld aus!')
    elif folder_path == "":
        messagebox.showerror('ERROR', 'Bitte geben Sie einen Speicherort an!')
    else:
        def download():
            try:
                p = Playlist(download_playlist)
                root.title('Downloading...')
                for video in p.videos:
                    video.streams.get_highest_resolution().download(folder_path)
                root.title('Download Complete! Download Another File...')
                download_entry.delete(0, END)
            except Exception as e:
                show_error_window(e)

        # Download in einem separaten Thread ausführen
        thread = threading.Thread(target=download)
        thread.start()


def download_mp3playlist():
    download_mp3playlist = download_entry.get()
    folder_path = path_entry.get()  # Speicherpfad aus dem Textfeld abrufen
    if download_mp3playlist == "":
        messagebox.showerror('ERROR', 'Bitte füllen Sie das Feld aus!')
    elif folder_path == "":
        messagebox.showerror('ERROR', 'Bitte geben Sie einen Speicherort an!')
    else:
        def download():
            try:
                p = Playlist(download_mp3playlist)
                root.title('Downloading...')
                for video in p.videos:
                    out_file = video.streams.filter(only_audio=True).first().download(folder_path)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                root.title('Download Complete! Download Another File...')
                download_entry.delete(0, END)
            except Exception as e:
                show_error_window(e)

        # Download in einem separaten Thread ausführen
        thread = threading.Thread(target=download)
        thread.start()


def select_path():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.delete(0, END)
        path_entry.insert(END, folder_path)


# Funktion zum Öffnen der Hilfe-Website
def open_help_website():
    webbrowser.open("https://github.com/JDLPIXEL/")


# GUI-Setup
root = tk.Tk()
root.title("Youtube Downloader [Vollversion 2.2 German]")

# Neuer IconBitmapCode //PNG
img = PhotoImage(file='iconmain.png')
root.tk.call('wm', 'iconphoto', root._w, img)
root.geometry("853x638")
root.resizable(width=0, height=0)
root.config(bg="#1f1f1f")
img = PhotoImage(file="yt_background.png")
label = Label(
    root,
    image=img
)
label.place(x=0, y=0)

# Paste-Button
paste_button = Button(root, text="Einfügen", command=lambda: download_entry.event_generate("<<Paste>>"), bg="#ff0000",
                      fg="white", font=("Helvetica", 14))
paste_button.place(relx=0.840, rely=0.250, anchor='center')


# Download-Buttons
mp4_button = Button(root, text="MP4 Download", command=download_start, bg="#ff0000", fg="white", font=("", 14))
mp4_button.place(relx=0.5, rely=0.5, anchor='center')
mp3_button = Button(root, text="MP3 Download", command=download_mp3, bg="#ff0000", fg="white", font=("", 14))
mp3_button.place(relx=0.5, rely=0.6, anchor='center')
playlist_button = Button(root, text="MP4 Playlist Download", command=download_playlist, bg="#ff0000", fg="white",
                         font=("Helvetica", 14))
playlist_button.place(relx=0.5, rely=0.7, anchor='center')
mp3playlist_button = Button(root, text="MP3 Playlist Download", command=download_mp3playlist, bg="#ff0000",
                            fg="white", font=("Helvetica", 14))
mp3playlist_button.place(relx=0.5, rely=0.8, anchor='center')

# Eingabefeld
download_entry = Entry(root, bd=5, width=40, bg="#adafad", fg="#000000", font=("Helvetica", 14))
download_entry.place(relx=0.5, rely=0.250, anchor='center')

# Menüleiste
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=root.quit)
menubar.add_cascade(label="Menü", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Hilfe", command=open_help_website)
menubar.add_cascade(label="Hilfe", menu=helpmenu)
root.config(menu=menubar)

# Footer
footer_label = tk.Label(root, text="© 2023 YouTube Downloader. Alle Rechte vorbehalten.", bg="#2A2A2A", fg="white",
                        font=("Helvetica", 10))
footer_label.place(x=0, y=595)

footer_label = tk.Label(root, text="➱Vollversion 2.2", bg="#2A2A2A", fg="white", font=("Helvetica", 10))
footer_label.place(x=0, y=571)

# Pfad auswählen
path_label = tk.Label(root, text="Speicherort auswählen:", bg="#1f1f1f", fg="white", font=("Helvetica", 12))
path_label.place(relx=0.5, rely=0.300, anchor='center')

path_entry = Entry(root, bd=5, width=40, bg="#adafad", fg="#000000", font=("Helvetica", 12))
path_entry.place(relx=0.5, rely=0.350, anchor='center')

path_button = Button(root, text="Pfad auswählen", command=select_path, bg="#ff0000", fg="white", font=("Helvetica", 12))
path_button.place(relx=0.5, rely=0.400, anchor='center')

root.mainloop()
