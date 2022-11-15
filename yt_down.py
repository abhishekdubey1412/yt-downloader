from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pytube import Playlist, YouTube
import os
import threading
import pathlib
from io import BytesIO
from urllib.request import urlopen

root = Tk()

# Set Default Width
root_width = 900

# Set Geometry, Minsize, Maxsize
root.wm_geometry(f"{root_width}x800")
root.wm_minsize(root_width, 800)
root.wm_maxsize(root_width, 800)

# Set Title, Icon
root.wm_title('Yt Downloader')
icon_name = 'icon.ico'
icon_path = os.path.abspath(icon_name)
root.wm_iconbitmap(icon_path)

# Create A Function For Give the Title OF link


def title():
    global get_input_var
    get_input_var = get_input.get()

    # Check Which type of link
    check_url_type = get_input_var.find('playlist')

    if check_url_type == -1:
        video_title = YouTube(get_input_var).title
        new_len = video_title.find(' ', 40)
        wt_len = video_title.find(' ', 80)
        title_one = video_title[:new_len] + '\n' + \
            video_title[new_len:wt_len].strip() + '\n' + \
            video_title[wt_len:].strip()
        title_two = video_title[:new_len] + \
            '\n' + video_title[new_len:].strip()
        if new_len == -1:
            title_label.config(text=video_title)
        elif wt_len == -1:
            title_label.config(text=title_two)
        else:
            title_label.config(text=title_one)
    else:
        video_title = Playlist(get_input_var).title
        new_len = video_title.find(' ', 40)
        wt_len = video_title.find(' ', 80)
        title_one = video_title[:new_len] + '\n' + \
            video_title[new_len:wt_len].strip() + '\n' + \
            video_title[wt_len:].strip()
        title_two = video_title[:new_len] + \
            '\n' + video_title[new_len:].strip()

        if new_len == -1:
            title_label.config(text=video_title)
        elif wt_len == -1:
            title_label.config(text=title_two)
        else:
            title_label.config(text=title_one)


def thumbnail_image_fun():
    if get_input_var.find('playlist') == -1:
        global thumbnail_image, yt
        yt = YouTube(get_input_var)
        # DISPLAYING THUMBNAIL
        url_imag = urlopen(yt.thumbnail_url).read()
        thumbnail_photo = Image.open(BytesIO(url_imag))
        resize_image = thumbnail_photo.resize((288, 162), Image.LANCZOS)
        thumbnail_image = ImageTk.PhotoImage(resize_image)
        canvas.itemconfig(thumnail_var, image=thumbnail_image)
    else:
        play_yt = Playlist(get_input_var)
        for url in play_yt.video_urls[:1]:
            global pl_thumbnail_image, pl_yt
            pl_yt = YouTube(url)
            # DISPLAYING THUMBNAIL
            pl_url_imag = urlopen(pl_yt.thumbnail_url).read()
            pl_thumbnail_photo = Image.open(BytesIO(pl_url_imag))
            pl_resize_image = pl_thumbnail_photo.resize((288, 162), Image.LANCZOS)
            pl_thumbnail_image = ImageTk.PhotoImage(pl_resize_image)
            canvas.itemconfig(thumnail_var, image=pl_thumbnail_image)

def video_down_btn():
    os.chdir(pathlib.Path.home() / "Downloads")
    if get_input_var.find('watch?') == -1:
        yt = Playlist(get_input_var)
        dir_name = str(yt.title)
        check_str = [':', '\\', '/', '*', '?', '"', '<', '>', '|']
        for i in check_str:
            if i in dir_name:
                dir_name = dir_name.replace(i, '_')
                if os.path.exists(dir_name):
                    os.chdir(dir_name)
                else:
                    os.mkdir(dir_name)
                    os.chdir(dir_name)
        for video in yt.videos:
            video.streams.get_highest_resolution().download()
        messagebox.showinfo(title='Yt Downloader',message='Downloading completed')
    else:
        YouTube(get_input_var).streams.get_highest_resolution().download()


def audio_down_btn():
    os.chdir(pathlib.Path.home() / "Downloads")
    if get_input_var.find('watch?') == -1:
        yt = Playlist(get_input_var)
        dir_name = str(yt.title) + ' ' + 'audio'
        check_str = [':', '\\', '/', '*', '?', '"', '<', '>', '|']
        for i in check_str:
            if i in dir_name:
                dir_name = dir_name.replace(i, '_')
                if os.path.exists(dir_name):
                    os.chdir(dir_name)
                else:
                    os.mkdir(dir_name)
                    os.chdir(dir_name)

        for url in yt.video_urls:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download()
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
    else:
        yt = YouTube(get_input_var)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

# Create A Function For Video MP4 Button


def video_button():
    title()

    thumbnail_image_fun()

    down_btn.config(text='Download Now', command=video_down_btn)

# Create A Function For Video MP4 Button


def audio_button():
    title()

    if get_input_var.find('playlist') == -1:
        thumbnail_image_fun()

    down_btn.config(text='Download Now', command=audio_down_btn)


# First Frame
first_height = 180
first_frame = Frame(root, width=root_width, height=first_height)

# Added JPG Photo using Pillow package
photo = Image.open("youtube-logo.png")
image = ImageTk.PhotoImage(photo)

# First Label
first_label = Label(first_frame, image=image, height=first_height)
first_label.pack()

# Sec Frame
sec_height = 100
sec_frame = Frame(root, width=root_width, height=sec_height)

# Entry Label
entry_label = Label(sec_frame, height=sec_height)
entry_label.pack(side=LEFT, anchor=CENTER)
# Set Entry
get_input = StringVar()
input_entry = Entry(entry_label, textvariable=get_input,
                    width=50, font=("Helvetica", 12, 'bold'))
input_entry.focus_force()
input_entry.pack(ipady=6)

# Set MP4 Label
vid_label = Label(sec_frame, height=sec_height)
vid_label.pack(side=LEFT, padx=9, anchor=CENTER, fill=BOTH)
# Set MP4 Button
video_btn = Button(vid_label, text='Video .MP4', font=("Helvetica", 12, 'bold'),
                   bg='black', fg='white', relief=FLAT, cursor='hand2', command=video_button)
video_btn.pack(ipadx=10, ipady=3)

# Set MP3 Label
aud_label = Label(sec_frame, height=100)
aud_label.pack(side=LEFT, anchor=CENTER, fill=BOTH)
# Set MP3 Button
audio_btn = Button(aud_label, text='Audio .MP3', font=("Helvetica", 12, 'bold'),
                   bg='black', fg='white', relief=FLAT, cursor='hand2', command=audio_button)
audio_btn.pack(ipadx=10, ipady=3)

# Third Frame
third_height = 250
third_frame = Frame(root, width=root_width, height=third_height)

# Create a canvas
canvas = Canvas(third_frame, width=288, height=162)
canvas.pack(side=LEFT, fill=Y, anchor=CENTER, padx=35, pady=40)

# Thumbnail PNG Photo using Pillow package
# Load an image in the script
thumbnail_photo = Image.open("thumbnail.png")
resize_image = thumbnail_photo.resize((288, 162), Image.LANCZOS)
thumbnail_image = ImageTk.PhotoImage(resize_image)

# Add image to the Canvas Items
thumnail_var = canvas.create_image(0, 0, anchor=NW, image=thumbnail_image)

# Title and Button Label
tb_label = Label(third_frame)
tb_label.pack(side=LEFT, anchor=CENTER)

# Set Title
title_label = Label(tb_label, text='Neque porro quisquam est qui dolorem ipsum \n quia dolor sit amet, consectetur, adipisci velit...',
                    font=("Helvetica", 12, 'bold'))
title_label.pack(side=TOP, pady=40)

# Set Download Button
down_btn = Button(tb_label, text='Download', font=(
    "Helvetica", 12, 'bold'), bg='black', fg='white', relief=FLAT, cursor='hand2')
down_btn.pack(side=BOTTOM, ipadx=10, ipady=3)

# Fourth Frame
fourth_frame = Frame(root, bg="green", width=root_width, height=70)

# Pause, Cancel Label
ps_label = Label(fourth_frame)
ps_label.pack(side=TOP)

# Pause Button
pause_button = Button(ps_label, text='Pause', font=(
    "Helvetica", 12, 'bold'), bg='black', fg='white', relief=FLAT, cursor='hand2')
pause_button.pack(side=LEFT, padx=20, ipadx=10, ipady=3)
# Cancel Button
cancel_button = Button(ps_label, text='Cancel', font=(
    "Helvetica", 12, 'bold'), bg='black', fg='white', relief=FLAT, cursor='hand2')
cancel_button.pack(side=LEFT, ipadx=10, ipady=3)

# Create A Scrollbar Main Frame
fifth_frame = Frame(root, width=root_width)

# First Frame Pack
first_frame.pack(side=TOP, fill=Y)
# Sec Frame Pack
sec_frame.pack(side=TOP, fill=Y)
# Third Frame Pack
third_frame.pack(side=TOP, fill=Y)
# Fourth Frame Pack
fourth_frame.pack(side=TOP, fill=Y)
# Fifth Frame Pack
fifth_frame.pack(side=TOP, fill=Y)

root.mainloop()