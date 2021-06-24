from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
root.title('Alexander\'s MP3 Player')

root.geometry("550x340")

pygame.mixer.init()

# Grab song length time info

def play_time():
    # Check if function continues running when it shouldn't
    if stopped:
        return
    # Grab elapsed time
    current_time = pygame.mixer.music.get_pos() /1000
    
    # temp label get data
    #slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')
    
    # Convert to time format
    converted_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
    

    # Grab song title from playlist
    song = song_box.get(ACTIVE)
    # Add directory structure and mp3 to song title
    song = f'C:/Users/antic/audio/{song}.mp3'
    # Load song length with Mutagen   
    song_mut = MP3(song)
    # Get song length
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))
    
    # Increase current time by 1 second to sync with slider
    current_time +=1
    
    
    if int(my_slider.get()) >= int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} / {converted_song_length}')
    
    elif paused:
        pass
    
    elif int(my_slider.get()) == int(current_time):
        # Slider hasn't been moved
        # Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    
    else:
        # slider has been moved
        # Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        # convert to time format
        slider_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))
        # output time to status bar
        status_bar.config(text=f'Time Elapsed: {slider_time} / {converted_song_length}')
        
        # Move by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
        
    
    
    # Update slider position value to current song position
    # my_slider.config(value=int(current_time))
    
    # update time
    status_bar.after(1000, play_time)
    
    
    
    



# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    
    # strip out dir info and extension from the song name
    song = song.replace("C:/Users/antic/audio/", "")
    song = song.replace(".mp3", "")
    
    # Add song to listbox
    song_box.insert(END, song)
    
# Add Many Songs
def add_songs():
    
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

    # Loop through songs

    for song in songs:
        # strip out dir info and extension from the song name
        song = song.replace("C:/Users/antic/audio/", "")
        song = song.replace(".mp3", "")
        
        # Add songs to listbox
        song_box.insert(END, song)

# Play Selected Song

def play():
    # Set stopped variable to false so song can play
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/antic/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # Call function to get song length
    play_time()
    
    # Update slider to position
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=0)
    
   
# Stop Playing Current Song
global stopped
stopped = False
def stop():
    # Clear the status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Stop song from playing
    pygame.mixer.music.stop()
    
    # Set stop variable to true
    
    global stopped
    stopped = True
    
    # Clear the select background box
    # song_box.selection_clear(ACTIVE)
    
# Create Global Pause Variable
global paused
paused = False
    
# Pause current song
def pause(is_paused):
    global paused
    is_paused = True
    
    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True
        
# Skip to the next song
def next_song():
    # Clear the status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Get the current song tuple number
    next_one = song_box.curselection()
    # Go to the next item on the list
    next_one = next_one[0]+1
    # Grab song title from playlist
    song = song_box.get(next_one)
    # Play next song
    song = f'C:/Users/antic/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # Clear active bar
    song_box.selection_clear(0, END)
    
    # Activate new song bar
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)
    
# Play previous song
def previous_song():
    # Clear the status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Get the current song tuple number
    next_one = song_box.curselection()
    # Go to the next item on the list
    next_one = next_one[0]-1
    # Grab song title from playlist
    song = song_box.get(next_one)
    # Play next song
    song = f'C:/Users/antic/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # Clear active bar
    song_box.selection_clear(0, END)
    
    # Activate new song bar
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)
    
# Delete a song
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    # Stop music if it's playing
    pygame.mixer.music.stop()
    
# Delete all songs
def delete_songs():
    stop()
    song_box.delete(0, END)
    # Stop music if it's playing
    pygame.mixer.music.stop()
 
# Create slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/antic/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=my_slider.get())
    
# Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    
    # Get current volume
    current_volume = pygame.mixer.music.get_volume()
    volume_frame.config(text=f'Vol :{(3 - len(str(int(current_volume * 100)))) * "  "} {int(current_volume * 100)}')
    
    # Change volume picture
    if current_volume <=.02:
        volume_meter.config(image=vol1)
    elif current_volume <= .33:
        volume_meter.config(image=vol2)
    elif current_volume <= .66:
        volume_meter.config(image=vol3)
    else:
        volume_meter.config(image=vol4)



# Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# Create Playlist Box
song_box = Listbox(master_frame, bg="white", fg="green", width=50, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

# Create Player Control Button Images
back_btn_img = PhotoImage(file='back_button.png')
forward_btn_img = PhotoImage(file='fwd_button.png')
play_btn_img = PhotoImage(file='play_button.png')
pause_btn_img = PhotoImage(file='pause_button.png')
stop_btn_img = PhotoImage(file='stop_button.png')

# Create Volume Control Images
global vol1
global vol2
global vol3
global vol4
vol1 = PhotoImage(file='volume1.png')
vol2 = PhotoImage(file='volume2.png')
vol3 = PhotoImage(file='volume3.png')
vol4 = PhotoImage(file='volume4.png')


# Create Player Control Frame

controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=10)

# Create Volume Meter Frame
volume_meter = Label(master_frame, image=vol4)
volume_meter.grid(row=1, column=1, padx=10)

# Create Volume Label Frame
volume_frame = LabelFrame(master_frame, text="Vol :     0")
volume_frame.grid(row=0, column=1, padx=8)

# Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=6)
forward_button.grid(row=0, column=1, padx=6)
play_button.grid(row=0, column=2, padx=6)
pause_button.grid(row=0, column=3, padx=6)
stop_button.grid(row=0, column=4, padx=6)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
# Add multiple songs
add_song_menu.add_command(label="Add Many Songs to Playlist", command=add_songs)

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove One Song from Playlist", command=delete_song)
remove_song_menu.add_command(label="Remove All Songs from Playlist", command=delete_songs)

# Create Status bar

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)



# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)




root.mainloop()

