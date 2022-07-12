from tkinter import * 
import sys, getpass, pygame , tkinter.font as _  , tkinter.ttk as ttk 
from tkinter import filedialog 
from mutagen.mp3 import MP3
import ctypes

myappid="dsffv"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
username = getpass.getuser()
paused = False
pygame.mixer.init()


def playsound(song):
    pygame.mixer.music.set_volume(volume.get()/100)
    pygame.mixer.music.stop()
    global paused
    paused = False
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    music_duration(song)

def play_pause(button):
    global pause_button, play_button
    if button == "pause" :
       pause_button.grid_forget()
       play_button.grid(row=0, column = 1)
    elif button == "play":
        play_button.grid_forget()
        pause_button.grid( row=0, column = 1)

def change_track(index):
    try:
      current_song_position = MUSIC_PLAYLIST.curselection()[0]
      next_song_position = current_song_position + index
      MUSIC_PLAYLIST.selection_clear(0, END)
      MUSIC_PLAYLIST.activate(next_song_position)
      MUSIC_PLAYLIST.select_set(next_song_position, last=None)
      song = MUSIC_PLAYLIST.get(ACTIVE)
      song = directory_list[next_song_position]
      playsound(song)
    except:
      MUSIC_PLAYLIST.activate(0)
      MUSIC_PLAYLIST.select_set(0, last=None)
      song = directory_list[0]
      playsound(song)
   
def music_duration(song):
  current = pygame.mixer.music.get_pos()/ 1000
  to =MP3(song).info.length
  BAR.config(to = to)
  BAR.set(current)
  BAR.after(1000 , lambda:music_duration(song) )  
    #

window = Tk()
window.geometry("650x550")
window.iconbitmap(sys.path[0] + "\\favicon.ico")
window.title("wink")
Helvetica = _.Font(family="Helvetica", size=10)


def src(name):
    relative_path = 'images\\' + name + "50.png"
    return PhotoImage(file=relative_path)

directory_list = []

def LIST_FILES():
    files = filedialog.askopenfilenames(initialdir=f'c:\\users\\{username}\\music', title="Choose song(s)",
                                     filetypes=(("mp3", "*.mp3"),))
    global directory_list
    # song_titles = [] 
    for track in files:
        directory_list += [track]
        print(directory_list)
        reverse_dir = track[::-1]
        title_reverse = reverse_dir[:reverse_dir.index('/')]
        title = title_reverse[::-1]
        MUSIC_PLAYLIST.insert(END, title)


MENU_BTN = Menu(window)
window.config(menu=MENU_BTN, bg="#fff")

browse = Menu(MENU_BTN)
MENU_BTN.add_cascade(label="OPTIONS", menu=browse)
browse.add_command(label="browse music", command=LIST_FILES)

MUSIC_PLAYLIST = Listbox(window, fg="#000", font=Helvetica, width=80, height=20, bd=0, highlightthickness=0)
MUSIC_PLAYLIST.pack(pady=12, padx=10)


MUSIC_BAR = Frame(window  , height = 5 , width = 350)
MUSIC_BAR.pack()
BAR = Scale(MUSIC_BAR , from_ = 0 , to = 100 , orient = HORIZONTAL , length  = 500  , width = 2.2 , fg = 'red' , showvalue = 0 , troughcolor = "black")
# BAR.config(state=DISABLED)
BAR.pack()

DIV_BTN = Frame(window, bg="#fff" , pady = 30)
DIV_BTN.pack()

PLAY = src("play")
PAUSE = src("pause")
STOP = src("stop")
NEXT = src("next")
PREVIOUS = src("previous")


# commands
def start():

    play_pause("play")
    
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        song = directory_list[MUSIC_PLAYLIST.curselection()[0]]
        playsound(song)


def halt():
    play_pause("pause")
    pygame.mixer.music.stop()
    global paused
    paused = False


def skip():
    play_pause("play")
    change_track(1)


def sigh():
    play_pause("pause")
    pygame.mixer.music.pause()
    global paused
    paused = True


def prior():
    play_pause("play")
    change_track(-1)


def control(img, command , column = None , asvariable = False):
    row = horizontal = 0
    BTN = Button(DIV_BTN, image=img, borderwidth = 0, command=command, cursor="hand2", bg="#fff")

    if asvariable == False:
        BTN.grid(row=row, column=column,padx=20, pady=10)
    else :return BTN




play_button = control(PLAY, start, asvariable=True)
play_button.grid(row = 0 , column = 1)
pause_button = control(PAUSE, sigh,  asvariable=True)
control(PREVIOUS, prior, 0)
control(NEXT, skip, 2)
control(STOP, halt, 3)

def volume_management(self ):
    pygame.mixer.music.set_volume(volume.get()/100)
volume = ttk.Scale(DIV_BTN, orient = HORIZONTAL , length = 140 , from_=0 , to = 100 , value = 30 ,command = volume_management)
volume.grid( row = 0, column = 6)

window.mainloop()
