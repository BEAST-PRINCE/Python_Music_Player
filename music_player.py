import os
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pygame
from mutagen.mp3 import MP3


global is_paused
is_paused = False

global stopped
stopped = False


root = tk.Tk()
root.geometry("800x540")


# Initialize PyGame Mixer
pygame.mixer.init()


# Song Lenght and Playing Time
def play_time():
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos()//1000
    if current_time<0:
        song_slider.config(value=0)
        current_time = current_time=time.strftime("%M:%S", time.gmtime(0))
    else:
        song_slider.config(value=current_time)
        current_time=time.strftime("%M:%S", time.gmtime(current_time))
    
    song = songlist.get(tk.ACTIVE)
    song = os.path.abspath('songs/'+song+'.mp3')
    song = song.replace("\\","/")
       
    statusbar.config(text=f'Time Elapsed:  {current_time}  of  {time_song_lenght}    ')

    if current_time>=time_song_lenght:
        next_song()

    statusbar.after(1000, play_time)


# Add Songs
def addSongs(multiple):
    if not multiple:
        song=filedialog.askopenfilename(initialdir='songs/', title="Choose a song", filetypes=(("mp3 file", "*.mp3"), ("wav file", "*.wav")))
        song_name=song.split('/')[-1].split('.')[0]
        songlist.insert(tk.END, song_name)
    else:
        songs = filedialog.askopenfilenames(initialdir='songs/', title="Choose a song", filetypes=(("mp3 file", "*.mp3"), ("wav file", "*.wav")))
        for song in songs:
            song_name=song.split('/')[-1].split('.')[0]
            songlist.insert(tk.END, song_name)


# Remlove Songs from Playlist
def del_songs(all):
    global stopped
    if not all:
        if songlist.get(tk.ANCHOR)==songlist.get(tk.ACTIVE):
            stopped = True
        songlist.delete(tk.ANCHOR)
        pygame.mixer.music.stop()
    else:
        stopped = True
        songlist.delete(0,tk.END)
        pygame.mixer.music.stop()
        statusbar.config(text='')
        

def change_song_length(cur_song):
    global song_lenght
    global time_song_lenght

    # Mutagen used
    song_mutagen = MP3(cur_song)
    song_lenght = song_mutagen.info.length
    time_song_lenght=time.strftime("%M:%S", time.gmtime(song_lenght))

    song_slider.config(to=int(song_lenght), value=0)


# Play the selected Song
def play():
    global stopped

    cur_song = songlist.get(tk.ACTIVE)
    songlist.selection_set(tk.ACTIVE)
    cur_song = os.path.abspath('songs/'+cur_song+'.mp3')
    cur_song=cur_song.replace("\\","/")

    change_song_length(cur_song)

    pygame.mixer.music.load(cur_song)
    pygame.mixer.music.play(loops=0)

    stopped = False

    play_time()
    
# Pause/Unpause the playing song
def pause(paused):
    global is_paused
    if not paused:
        pygame.mixer.music.pause()
        is_paused=True
    else:
        pygame.mixer.music.unpause()
        is_paused=False
        play_time()
        

# Stop the playing Song
def stop():
    global stopped

    song_slider.config(value=0)
    pygame.mixer.music.stop()

    stopped = True
    
    songlist.selection_clear(tk.ACTIVE)
    statusbar.config(text='')


# Plat Next Song
def next_song():
    global is_paused

    cur_song = songlist.curselection()
    next_song = cur_song[0]+1

    songlist.selection_clear(tk.ACTIVE)
    
    if songlist.size()>next_song:
        songlist.activate(next_song)
        songlist.selection_set(next_song)

        next_song = songlist.get(next_song)
        cur_song = os.path.abspath('songs/'+next_song+'.mp3')
        cur_song=cur_song.replace("\\","/")

        change_song_length(cur_song)

        pygame.mixer.music.load(cur_song)
        pygame.mixer.music.play(loops=0)

        is_paused = False
    else:
        pygame.mixer.music.stop()
        songlist.update()


# Play Previous Song
def prev_song():
    global is_paused

    cur_song = songlist.curselection()
    next_song = cur_song[0]-1

    if next_song>=0:
        songlist.selection_clear(tk.ACTIVE)
    
        songlist.activate(next_song)
        songlist.selection_set(next_song)

        next_song = songlist.get(next_song)
        cur_song = os.path.abspath('songs/'+next_song+'.mp3')
        cur_song=cur_song.replace("\\","/")

        change_song_length(cur_song)

        pygame.mixer.music.load(cur_song)
        pygame.mixer.music.play(loops=0)
        is_paused=False
    else:
        pygame.mixer.music.stop()
        songlist.update()


# Slider Control
# def slide(x):
#     print(int(song_slider.get()))
#     cur_song = songlist.get(tk.ACTIVE)
#     songlist.selection_set(tk.ACTIVE)
#     cur_song = os.path.abspath('songs/'+cur_song+'.mp3')
#     cur_song=cur_song.replace("\\","/")

#     pygame.mixer.music.load(cur_song)
#     pygame.mixer.music.play(loops=0,start=song_slider.getint())


# Volume Control
def slide_volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())




# PLaylist - ListBox
songlist = tk.Listbox(root, bg="#222020", fg="#ff4000", width=100, selectbackground="#ffff00",selectforeground="#e60000", font=("Helvetica", 14))
songlist.pack(fill='both', pady=20, padx=15)


# Music Player Control Buttons
stop_img = tk.PhotoImage(file='images/stop8.png')
play_img = tk.PhotoImage(file=os.path.abspath('images/play8.png'))
pause_img = tk.PhotoImage(file='images/pause8.png')
forward_img = tk.PhotoImage(file='images/skip8_right.png')
backward_img = tk.PhotoImage(file='images/skip8_left.png')


control_frame = tk.Frame(root)
control_frame.pack(pady=10)


play_btn = tk.Button(control_frame, image= play_img, borderwidth=2, command=play)
pause_btn = tk.Button(control_frame, image= pause_img, borderwidth=2, command=lambda: pause(is_paused))
forward_btn = tk.Button(control_frame, image= forward_img, borderwidth=2, command=next_song)
backward_btn = tk.Button(control_frame, image= backward_img, borderwidth=2, command=prev_song)
stop_btn = tk.Button(control_frame, image= stop_img, borderwidth=2, command=stop)

# Volume Frame
volume_frame = tk.LabelFrame(control_frame, text='Volume')
volume_frame.grid(row=0, column=0, padx=30)

# Volume Control Slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient='vertical', value=1, length=110, command=slide_volume)
volume_slider.pack()

backward_btn.grid(row=0,column=1, padx=15)
play_btn.grid(row=0,column=2, padx=15)
pause_btn.grid(row=0,column=3, padx=15)
stop_btn.grid(row=0,column=4, padx=15)
forward_btn.grid(row=0,column=5, padx=15)


# Menubar
menubar = tk.Menu(root,tearoff=False)
root.config(menu=menubar)

# Add Songs Menu
add_song = tk.Menu(menubar,tearoff=False)
menubar.add_cascade(label='Add Songs', menu=add_song)
add_song.add_command(label='Add One song to Playlist', command=lambda: addSongs(False))
add_song.add_command(label='Add Many songs to Playlist', command=lambda: addSongs(True))

# REmove Songs Menu
remove_song = tk.Menu(menubar,tearoff=False)
menubar.add_cascade(label='Remove Songs', menu=remove_song)
remove_song.add_command(label='Remove Song from Playlist',command=lambda: del_songs(False))
remove_song.add_command(label='Remove All Song from Playlist',command=lambda: del_songs(True))


# Song Slider
song_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal',value=0, length=630)
song_slider.pack(pady=25)


# Status Bar showing Song Progress
statusbar = tk.Label(root, text='', borderwidth=3, relief=tk.GROOVE, anchor=tk.E)
statusbar.pack(fill=tk.X, side=tk.BOTTOM, ipady=5, ipadx=10)




root.mainloop()