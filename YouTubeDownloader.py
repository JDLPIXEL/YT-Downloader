from pytube import YouTube
from pytube import Playlist
import os
import sys
from tkinter import messagebox
from tkinter import *
from tkinter import font
import tkinter as tk
from PIL import ImageTk, Image
import threading
import tkinter.filedialog as filedialog
import webbrowser
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
import json
from configparser import ConfigParser
import traceback
from datetime import datetime


# GUI-Setup
root = tk.Tk()
root.title("Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]")

# Neuer IconBitmapCode //PNG
img = PhotoImage(file='iconmain.png')
root.tk.call('wm', 'iconphoto', root._w, img)
root.geometry("853x638")
root.resizable(width=0, height=0)
root.config(bg="#1f1f1f")

img = PhotoImage(file="background.png")
background_label = Label(root, image=img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Pfad auswählen
path_label = tk.Label(root, text="Speicherort auswählen:", bg="#1f1f1f", fg="white", font=("Helvetica", 12))
path_label.place(relx=0.5, rely=0.300, anchor='center')

path_entry = Entry(root, bd=5, width=40, bg="#adafad", fg="#000000", font=("Helvetica", 12))
path_entry.place(relx=0.5, rely=0.350, anchor='center')



# Eingabefeld
download_entry = Entry(root, bd=5, width=40, bg="#adafad", fg="#000000", font=("Helvetica", 14))
download_entry.place(relx=0.5, rely=0.250, anchor='center')

# Funktion zum Anzeigen des Fehlerfensters
def show_error_window(error):
    # Erstelle ein neues Tkinter-Fenster
    
    error_window = tk.Toplevel()
    error_window.title("Fehler aufgetreten:")
    

    # Setze das Fensterlogo
    icon_path = "iconmain.png"
    if os.path.exists(icon_path):
        error_window.iconphoto(True, tk.PhotoImage(file=icon_path))

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

    # Funktion zum Ausblenden des Texts und Schließen des Fensters
    def close_text():
        download_label.pack_forget()
        close_button.pack_forget()
        error_window.destroy()

    # Erstelle den Schließen-Button
    close_button = tk.Button(error_window, text="Schließen", command=close_text)
    close_button.pack(pady=10)

    # Hauptfenster deaktivieren, während das Fehlerfenster geöffnet ist
    error_window.transient(root)
    error_window.grab_set()
    root.wait_window(error_window)
    close_text()
    root.title("Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]")



def save_download_history(title, folder_path):
    config = ConfigParser()

    try:
        # Überprüfen, ob die verlauf.ini-Datei bereits existiert
        if os.path.exists("verlauf.ini"):
            # Laden der vorhandenen Konfigurationsdatei
            config.read("verlauf.ini")

        # Hinzufügen des aktuellen Downloads zum Verlauf
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        section_name = f"Download {len(config.sections()) + 1}"
        config[section_name] = {
            "Title": title,
            "Folder Path": folder_path,
            "Downloaded At": current_time
        }

        # Speichern der aktualisierten Konfigurationsdatei
        with open("verlauf.ini", "w") as config_file:
            config.write(config_file)

    except Exception as e:
        show_error_window(e)

    

    # Speichern der aktualisierten Konfigurationsdatei
    with open("verlauf.ini", "w") as config_file:
        config.write(config_file)

def save_download_path_last(folder_path):
    # Speichern des ausgewählten Ordnerpfads in einer Konfigurationsdatei
    config = ConfigParser()
    config['PATH'] = {'DownloadPath': folder_path}
    with open('path.ini', 'w') as configfile:
        config.write(configfile)


def display_saved_path():
    if os.path.exists("path.ini"):
        config = ConfigParser()
        config.read("path.ini")

        if 'PATH' in config and 'DownloadPath' in config['PATH']:
            saved_path = config['PATH']['DownloadPath']
            path_entry.delete(0, 'end')  # Vorherigen Inhalt im Feld löschen
            path_entry.insert(0, saved_path)  # Gespeicherten Pfad in das Feld einfügen
        

display_saved_path()  # Aufrufen der Funktion, um den gespeicherten Pfad anzuzeigen


from tkinter import *
from tkinter import messagebox
import threading
import os
from PIL import Image, ImageTk

# ...

def download_start():
    download_link = download_entry.get()
    folder_path = path_entry.get()  # Speicherpfad aus dem Textfeld abrufen
    if download_link == "":
        messagebox.showerror('ERROR', 'Bitte füllen Sie das Feld aus!')
    elif folder_path == "":
        messagebox.showerror('ERROR', 'Bitte geben Sie einen Speicherort an!')
    else:
        download_window = None
        
        def delete_complete_text():
            download_label.configure(text="")
            close_text()
            download_window.after(10, download_window.destroy)  # Fenster nach 10 Sekunden schließen
        def close_text():
            download_label.pack_forget()
            close_button.pack_forget()
            download_window.destroy()  # Fenster schließen

        def download():
            save_download_history(download_link, folder_path)
            save_download_path_last(folder_path)
            global download_label
            global close_button
            nonlocal download_window

            try:
                mp4_button.config(state="disabled")
                mp3_button.config(state="disabled")
                playlist_button.config(state="disabled")
                mp3playlist_button.config(state="disabled")

                yt = YouTube(download_link)
                root.title('Downloading...')

                download_window = Toplevel(root)  # Erstellen Sie das Download-Fenster

                # Setze das Fensterlogo
                icon_path = "iconmain.png"
                if os.path.exists(icon_path):
                    img = ImageTk.PhotoImage(file=icon_path)
                    download_window.iconphoto(True, img)

                download_window.title('Download')
                download_window.geometry('500x300')
                download_window.resizable(False, False)

                download_label = Label(download_window, text="Downloading...", font=("Arial", 14, "bold"), fg="red")
                download_label.pack(pady=20)

                # Laden und Anzeigen des GIFs mit Pillow
                gif_path = "download.gif"
                if os.path.exists(gif_path):
                    gif_image = Image.open(gif_path)
                    gif_frames = []
                    try:
                        while True:
                            gif_frames.append(gif_image.copy())
                            gif_image.seek(len(gif_frames))  # Nächstes Frame laden
                    except EOFError:
                        pass

                    # Anzeigen des animierten GIFs
                    gif_label = Label(download_window)
                    gif_label.pack()
                    gif_index = 0

                    def update_gif_label():
                        nonlocal gif_index
                        gif_frame = gif_frames[gif_index]
                        gif_index = (gif_index + 1) % len(gif_frames)
                        gif_photo = ImageTk.PhotoImage(gif_frame)
                        gif_label.configure(image=gif_photo)
                        gif_label.image = gif_photo
                        download_window.after(100, update_gif_label)  # Aktualisierung alle 100 Millisekunden
                    update_gif_label()

                video = yt.streams.get_highest_resolution()
                video.download(folder_path)

                # Hänge den Text an den Dateinamen an
                file_name = video.default_filename
                new_file_name = os.path.splitext(file_name)[0] + "- Downloaded by JDL_YouTube_Downloader" + os.path.splitext(file_name)[1]
                os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))

                download_label.configure(text="Download Complete!")
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")
                root.title('Youtube Downloader [Vollversion 2.2 German]')
                close_button = Label(download_window, text="X", font=("Arial", 14, "bold"), fg="black", bg="white")
                close_button.pack()
                close_button.bind("<Button-1>", lambda event: close_text())

                # Text nach 10 Sekunden automatisch löschen
                download_window.after(10000, delete_complete_text)

                download_entry.delete(0, END)
            except Exception as e:
                root.title('Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]')
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")
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
        download_window = None

        def delete_complete_text():
            download_label.configure(text="")
            close_text()
            download_window.after(10, download_window.destroy)  # Fenster nach 10 Sekunden schließen

        def close_text():
            download_label.pack_forget()
            close_button.pack_forget()
            download_window.destroy()  # Fenster schließen

        def download():
            save_download_history(download_mp3, folder_path)
            save_download_path_last(folder_path)
            global download_label
            global close_button
            nonlocal download_window

            try:
                mp4_button.config(state="disabled")
                mp3_button.config(state="disabled")
                playlist_button.config(state="disabled")
                mp3playlist_button.config(state="disabled")

                yt = YouTube(download_mp3)
                root.title('Downloading...')

                download_window = Toplevel(root)  # Erstellen Sie das Download-Fenster

                # Setze das Fensterlogo
                icon_path = "iconmain.png"
                if os.path.exists(icon_path):
                    img = tk.PhotoImage(file=icon_path)
                    download_window.iconphoto(True, img)

                download_window.title('Download')
                download_window.geometry('300x100')
                download_window.resizable(False, False)

                download_label = Label(download_window, text="Downloading...", font=("Arial", 14, "bold"), fg="red")
                download_label.pack(pady=20)

                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(folder_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + ' - Downloaded by JDL_YT_Downloader' + '.mp3'
                os.rename(out_file, new_file)
                
                download_label.configure(text="Download Complete!")
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")
                root.title('Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]')
                close_button = Label(download_window, text="X", font=("Arial", 14, "bold"), fg="black", bg="white")
                close_button.pack()
                close_button.bind("<Button-1>", lambda event: close_text())

                # Text nach 10 Sekunden automatisch löschen
                download_window.after(10000, delete_complete_text)

                download_entry.delete(0, END)
            except Exception as e:
                root.title('Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]')
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")
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
        download_window = None

        def delete_complete_text():
            download_label.configure(text="")
            close_text()
            download_window.after(10, download_window.destroy)  # Fenster nach 10 Sekunden schließen

        def close_text():
            download_label.pack_forget()
            close_button.pack_forget()
            download_window.destroy()  # Fenster schließen

        def download():
            save_download_history(download_playlist, folder_path)
            save_download_path_last(folder_path)
            global download_label
            global close_button
            nonlocal download_window

            try:
                mp4_button.config(state="disabled")
                mp3_button.config(state="disabled")
                playlist_button.config(state="disabled")
                mp3playlist_button.config(state="disabled")
                p = Playlist(download_playlist)
                root.title('Downloading...')

                download_window = Toplevel(root)  # Erstellen Sie das Download-Fenster

                # Setze das Fensterlogo
                icon_path = "iconmain.png"
                if os.path.exists(icon_path):
                    img = tk.PhotoImage(file=icon_path)
                    download_window.iconphoto(True, img)

                download_window.title('Download')
                download_window.geometry('300x100')
                download_window.resizable(False, False)

                download_label = Label(download_window, text="Downloading...", font=("Arial", 14, "bold"), fg="red")
                download_label.pack(pady=20)

                for video in p.videos:
                    video.streams.get_highest_resolution().download(folder_path)
                    base, ext = os.path.splitext(video.title)
                    new_file = os.path.join(folder_path, base + ' - Downloaded by JDL_YT_Downloader' + ext)
                    os.rename(os.path.join(folder_path, video.title), new_file)

                download_label.configure(text="Download Complete!")
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")
                root.title('Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]')
                close_button = Label(download_window, text="X", font=("Arial", 14, "bold"), fg="black", bg="white")
                close_button.pack()
                close_button.bind("<Button-1>", lambda event: close_text())

                # Text nach 10 Sekunden automatisch löschen
                download_window.after(10000, delete_complete_text)

                download_entry.delete(0, END)
            except Exception as e:
                show_error_window(e)
                root.title('Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]')
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")

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
        download_window = None

        def delete_complete_text():
            download_label.configure(text="")
            close_text()
            download_window.after(10, download_window.destroy)  # Fenster nach 10 Sekunden schließen

        def close_text():
            download_label.pack_forget()
            close_button.pack_forget()
            download_window.destroy()  # Fenster schließen

        def download():
            save_download_history(download_mp3playlist, folder_path)
            save_download_path_last(folder_path)
            global download_label
            global close_button
            nonlocal download_window

            try:
                mp4_button.config(state="disabled")
                mp3_button.config(state="disabled")
                playlist_button.config(state="disabled")
                mp3playlist_button.config(state="disabled")
                p = Playlist(download_mp3playlist)
                root.title('Downloading...')

                download_window = Toplevel(root)  # Erstellen Sie das Download-Fenster

                # Setze das Fensterlogo
                icon_path = "iconmain.png"
                if os.path.exists(icon_path):
                    img = tk.PhotoImage(file=icon_path)
                    download_window.iconphoto(True, img)

                download_window.title('Download')
                download_window.geometry('300x100')
                download_window.resizable(False, False)

                download_label = Label(download_window, text="Downloading...", font=("Arial", 14, "bold"), fg="red")
                download_label.pack(pady=20)

                for video in p.videos:
                    out_file = video.streams.filter(only_audio=True).first().download(folder_path)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + ' - Downloaded by JDL_YT_Downloader' + '.mp3'
                    os.rename(out_file, new_file)

                download_label.configure(text="Download Complete!")
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")
                root.title('Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]')
                close_button = Label(download_window, text="X", font=("Arial", 14, "bold"), fg="black", bg="white")
                close_button.pack()
                close_button.bind("<Button-1>", lambda event: close_text())

                # Text nach 10 Sekunden automatisch löschen
                download_window.after(10000, delete_complete_text)

                download_entry.delete(0, END)
            except Exception as e:
                root.title('Youtube Downloader [Beta-Version 2.3 German | Lizensiert für /06072023]')
                mp4_button.config(state="normal")
                mp3_button.config(state="normal")
                playlist_button.config(state="normal")
                mp3playlist_button.config(state="normal")
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
def open_help_mail():
    webbrowser.open("https://github.com/JDLPIXEL/")

#Path-Button
path_button = Button(root, text="Pfad auswählen", command=select_path, bg="#ff0000", fg="white", font=("Helvetica", 12))
path_button.place(relx=0.5, rely=0.400, anchor='center')

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


# Paste-Button
paste_button = Button(root, text="Einfügen", command=lambda: download_entry.event_generate("<<Paste>>"), bg="#ff0000",
                      fg="white", font=("Helvetica", 14))
paste_button.place(relx=0.840, rely=0.250, anchor='center')


def show_download_history():
    # Überprüfen, ob die verlauf.ini-Datei existiert
    if not os.path.exists("verlauf.ini"):
        messagebox.showinfo("Download-Verlauf", "Kein Download-Verlauf vorhanden.")
        return

    # Laden der Konfigurationsdatei
    config = ConfigParser()
    config.read("verlauf.ini")

    # Erstellen eines neuen Fensters
    history_window = tk.Toplevel(root)
    history_window.title("Download-Verlauf")
    # Setze das Fensterlogo
    icon_path = "iconmain.png"
    if os.path.exists(icon_path):
        history_window.iconphoto(True, tk.PhotoImage(file=icon_path))

    # Erstellen eines Scrollbereichs
    scrollbar = tk.Scrollbar(history_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Erstellen eines Textfelds für die Anzeige des Download-Verlaufs
    history_text = tk.Text(history_window, yscrollcommand=scrollbar.set)
    history_text.pack(fill=tk.BOTH, expand=True)

    # Schleife über alle Abschnitte in der Konfigurationsdatei
    for section_name in config.sections():
        # Auslesen der Informationen für jeden Download
        title = config.get(section_name, "Title")
        folder_path = config.get(section_name, "Folder Path")
        downloaded_at = config.get(section_name, "Downloaded At")

        # Hinzufügen der Informationen zum Textfeld
        history_text.insert(tk.END, f"Download {section_name}:\n")
        history_text.insert(tk.END, f"Title: {title}\n")
        history_text.insert(tk.END, f"Folder Path: {folder_path}\n")
        history_text.insert(tk.END, f"Downloaded At: {downloaded_at}\n")
        history_text.insert(tk.END, "-" * 20 + "\n")

    # Scrollen im Textfeld ermöglichen
    scrollbar.config(command=history_text.yview)

# Funktion für die Website
def open_help_website(): webbrowser.open("http://jdlpixel.de/download"
                                         )
# Menüleiste
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.configure(bg="#1f1f1f", fg="white")
filemenu.add_command(label="Beenden", command=root.quit)
menubar.add_cascade(label="Menü", menu=filemenu)
filemenu.add_command(label="Download-Verlauf", command=show_download_history)




helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Kontakt", command=open_help_mail)

helpmenu.add_command(label="Website", command=open_help_website)
menubar.add_cascade(label="Hilfe", menu=helpmenu)

root.config(menu=menubar)



# Menü "Features"
features_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Features", menu=features_menu)

# Untermenü "Lichtauswahl"
light_menu = Menu(features_menu, tearoff=0)
features_menu.add_cascade(label="Allgemeine Farbauswahl", menu=light_menu)


# Optionen für die Farbauswahl
button_color = tk.StringVar()
button_color.set("Rot (Standard)")  # Standardwert



text_color = tk.StringVar()
text_color.set("Rot (Standard)")  # Standardwert

ueberschrift = tk.Label(root, text="YouTube_Downloader.exe", bg="#1f1f1f", fg="red",
                        font=("System",54))
ueberschrift.place(relx=0.5, rely=-0.42, anchor='center')
ueberschrift.place(x=0, y=300)

def change_text_color():
    color = text_color.get()
    save_configuration()
    text_colors = {
        "Grün": "green",
        "Blau": "blue",
        "Rot (Standard)": "#ff0000",
        "Gelb": "yellow",
        "Lila": "purple"
    }

    text_color_code = text_colors.get(color, "#ff0000")
    ueberschrift.config(fg=text_color_code)
    save_configuration()


ueberschrift_jdl = tk.Label(root, text="⠀by JDL_PIXEL  / BETA-VERSION", bg="#1f1f1f", fg="white",
                        font=("System",30, 'italic'))
ueberschrift_jdl.place(relx=0.5, rely=-0.36)
ueberschrift_jdl.place(x=-448, y=300)



    



# Untermenü "TextFarbe YouTube_Downloader.exe"
text_color_menu = Menu(features_menu, tearoff=0)
features_menu.add_cascade(label="LogoFarbe", menu=text_color_menu)

text_color_menu.add_radiobutton(label="Lila", variable=text_color, command=change_text_color)
text_color_menu.add_radiobutton(label="Gelb", variable=text_color, command=change_text_color)
text_color_menu.add_radiobutton(label="Rot (Standard)", variable=text_color, command=change_text_color)
text_color_menu.add_radiobutton(label="Grün", variable=text_color, command=change_text_color)
text_color_menu.add_radiobutton(label="Blau", variable=text_color, command=change_text_color)

def change_button_colors():
    color = button_color.get()
    save_configuration()
    button_colors = {
        "Grün": "green",
        "Blau": "blue",
        "Rot (Standard)": "#ff0000",
        "Gelb": "yellow",
        "Lila": "purple"
    }

    button_color_code = button_colors.get(color, "#ff0000")

    if color == "Gelb":
        bg_color = "yellow"
        fg_color = "black"
    else:
        bg_color = button_color_code
        fg_color = "white"

    mp4_button.config(bg=bg_color, fg=fg_color)
    mp3_button.config(bg=bg_color, fg=fg_color)
    playlist_button.config(bg=bg_color, fg=fg_color)
    mp3playlist_button.config(bg=bg_color, fg=fg_color)
    paste_button.config(bg=bg_color, fg=fg_color)
    path_button.config(bg=bg_color, fg=fg_color)

    save_configuration()  # Speichern der Konfiguration




light_menu.add_radiobutton(label="Grün", variable=button_color, command=change_button_colors)
light_menu.add_radiobutton(label="Blau", variable=button_color, command=change_button_colors)
light_menu.add_radiobutton(label="Rot (Standard)", variable=button_color, command=change_button_colors)
light_menu.add_radiobutton(label="Gelb", variable=button_color, command=change_button_colors)
light_menu.add_radiobutton(label="Lila", variable=button_color, command=change_button_colors)



def open_background_image():
    filepath = filedialog.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    if filepath:
        try:
            # Bild laden
            image = Image.open(filepath)
            # Bildgröße anpassen
            resized_image = image.resize((853, 638), Image.ANTIALIAS)
            # Bild als PhotoImage konvertieren
            bg_image = ImageTk.PhotoImage(resized_image)
            # Hintergrundbild des root-Fensters setzen
            root.configure(background='')
            root.configure(background='#1f1f1f')  # Hintergrundfarbe setzen
            background_label.configure(image=bg_image)
            background_label.image = bg_image  # Referenz speichern, um Garbage Collection zu verhindern
            background_label.image_path = filepath  # Speichern des Pfads des Hintergrundbildes
            save_configuration()  # Speichern der Konfiguration
        except Exception as e:
            show_error_window(e)


# Hintergrund-Untermenü
background_menu = Menu(features_menu, tearoff=0)
features_menu.add_cascade(label="Hintergrund", menu=background_menu)
background_menu.add_command(label="Hintergrundbild auswählen", command=open_background_image)

#Reset Background-IMG
def reset_background_image():
    img = PhotoImage(file="background.png")
    background_label.configure(image=img)
    background_label.image = img
    default_image = "background.png"
    config = ConfigParser()
    config.read("config.ini")
    config.set("Appearance", "backgroundimage", default_image)
    with open("config.ini", "w") as config_file:
        config.write(config_file)

def reset_to_defaults():
    reset_background_image()
    reset_button_colors()
    
#Standartwere wiederherstellen
background_menu.add_command(label="Hintergrundbild zurücksetzen", command=reset_background_image)

features_menu.add_command(label="Auf Standardwerte zurücksetzen", command=reset_to_defaults)

# Footer
footer_label = tk.Label(root, text="© 2023 YouTube Downloader. Alle Rechte vorbehalten.", bg="#2A2A2A", fg="white",
                        font=("Helvetica", 10))
footer_label.place(x=0, y=595)

footer_label = tk.Label(root, text="➱Beta-Version 2.3 German | Lizensiert für /06072023", bg="#2A2A2A", fg="white", font=("Helvetica", 10))
footer_label.place(x=0, y=571)





def reset_button_colors():
    button_color.set("Rot (Standard)")
    change_button_colors()
    text_color.set("Rot (Standard)")
    change_text_color()
    default_image = "background.png"
    config = ConfigParser()
    config.read("config.ini")
    config.set("Appearance", "backgroundimage", default_image)
    with open("config.ini", "w") as config_file:
        config.write(config_file)







def save_configuration():
    try:
        config = ConfigParser()
        config['Appearance'] = {
            'ButtonColor': button_color.get(),
            'TextColor': text_color.get(),
            'BackgroundImage': background_label.image_path
            
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        traceback.print_exc()




def load_configuration():
    try:
        config = ConfigParser()
        config.read('config.ini')

        # Hintergrundfarbe laden
        button_color.set(config.get('Appearance', 'ButtonColor'))
        change_button_colors()

        # Textfarbe laden
        text_color_value = config.get('Appearance', 'TextColor')
        if text_color_value:
            text_color.set(text_color_value)
            change_text_color()

        # Hintergrundbild laden
        
        background_image = config.get('Appearance', 'BackgroundImage')
        if background_image:
            image = Image.open(background_image)
            resized_image = image.resize((853, 638), Image.ANTIALIAS)
            bg_image = ImageTk.PhotoImage(resized_image)
            root.configure(background='')
            root.configure(background='#1f1f1f')
            background_label.configure(image=bg_image)
            background_label.image = bg_image
            background_label.image_path = background_image

    

    except Exception as e:
        traceback.print_exc()



load_configuration()


root.mainloop()