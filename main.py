from tkinter import * 
import sys, getpass, pygame , tkinter.font as _  , tkinter.ttk as ttk 
from tkinter import filedialog 
from mutagen.mp3 import MP3
import ctypes
from PIL import Image, ImageTk
import webbrowser

myappid="Daniel.Kenan.Slinda"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
username = getpass.getuser()
window = Tk()
window.resizable(False,False)
window.geometry("650x550")
favicon = sys.path[0] + "\\favicon.ico"
window.iconbitmap(favicon)
window.title("Wink")
Helvetica = _.Font(family="Helvetica", size=11)

paused = False
current_song = None
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
  if current == to: #not working at the moment
    if len(directory_list) :
        current_song_position = MUSIC_PLAYLIST.curselection()[0]
        next_song_position = current_song_position + 1
        MUSIC_PLAYLIST.activate(next_song_position)
        skip()
    
    return 
  BAR.set(current)
  BAR.config(to = to)
  BAR.after(100 , lambda:music_duration(song) )
   

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
        # print(directory_list)
        reverse_dir = track[::-1]
        title_reverse = reverse_dir[:reverse_dir.index('/')]
        title = title_reverse[::-1]
        MUSIC_PLAYLIST.insert(END, title)

MENU_BTN = Menu(window)
window.config(menu=MENU_BTN, bg="#fff")

def icon(image):
    img = Image.open(sys.path[0]+'\\images\\' + image +".png")
    return ImageTk.PhotoImage(img)

def info_popup():
    window = Toplevel()
    window.title('info')
    global favicon
    window.iconbitmap(favicon)
    window.geometry('300x300')
    text = Text(window)
    text.tag_configure('name',justify='center')
    text.insert('1.0','\n')
    text.insert('2.0',u'\u00A9'+'Daniel Kenan Slinda\n\n')
    text.insert('3.0','www.github.com/daniel-kenan\n\n' )
    text.insert('5.0','MY WEBSITE\n')
    text.insert('6.0','www.danielslinda.art'  )
    text.tag_add('name','2.0','end')
    text.pack()

def gotoURL():
    webbrowser.open('danielslinda.art')

NAV_MENU ,HELP_MENU ,OPTION_MENU = Menu(MENU_BTN),Menu(MENU_BTN),Menu(MENU_BTN)
MENU_BTN.add_cascade(label="File", menu=NAV_MENU)
MENU_BTN.add_cascade(label="Options",menu=OPTION_MENU)
MENU_BTN.add_cascade(label="Help", menu=HELP_MENU )

info,music,donate = icon('info') , icon('audio'), icon('donate')

HELP_MENU.add_command(label="Info",image=info,compound='left',command=info_popup)
NAV_MENU.add_command(label="Add music to playlist", image=music , compound='left', command=LIST_FILES)
NAV_MENU.add_command(label="Donate", image=donate , compound='left', command=gotoURL)
OPTION_MENU.add_command(label="Donate", image=donate , compound='left', command=gotoURL)
HELP_MENU.add_command(label="Donate", image=donate , compound='left', command=gotoURL)
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

def start():
    if not len(directory_list) or not len(MUSIC_PLAYLIST.curselection()[:]): return    
    play_pause("play")
    global paused ,current_song
    highlighted_song =  directory_list[MUSIC_PLAYLIST.curselection()[0]]
    
    if paused and current_song == highlighted_song:
        pygame.mixer.music.unpause()
        paused = False
    else:
        song = directory_list[MUSIC_PLAYLIST.curselection()[0]]
        current_song=song
        playsound(song)
        
def pause():
    play_pause("pause")
    pygame.mixer.music.stop()
    global paused
    paused = False

def skip():
    if current_song == None or not len(MUSIC_PLAYLIST.curselection()):return
    play_pause("play")
    change_track(1)

def sigh():
    play_pause("pause")
    pygame.mixer.music.pause()
    global paused
    paused = True

def prior():
    global current_song
    if current_song == None or not len(MUSIC_PLAYLIST.curselection()):return
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

control( img= PREVIOUS, command= prior, column  = 0)
control( img= NEXT, command= skip, column= 2)
control( img= STOP, command = pause, column= 3)

def volume_management(self ):
    pygame.mixer.music.set_volume(volume.get()/100)

volume = ttk.Scale(DIV_BTN, orient = HORIZONTAL , length = 140 , from_=0 , to = 100 , value = 30 ,command = volume_management)
volume.grid( row = 0, column = 6)

window.mainloop()
