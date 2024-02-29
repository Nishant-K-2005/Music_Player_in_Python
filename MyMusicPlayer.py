#-------------Importing All Modules------------------
import tkinter
import mysql.connector as _connection
from pygame import mixer
import tkinter.messagebox as tkmsg
#----------------------------------------------------
#Establishing the connection between Mysql and Python  
link = _connection.connect(
    host="localhost", user="root", password='1234'
    )
_cursor = link.cursor() #Setting the Cursor

#----CREATING DATABASE IF DO NOT EXISTS ALREADY------
try:
    _cursor.execute("CREATE DATABASE SONGDB")
    _cursor.execute("USE SONGDB")
    _cursor.execute("CREATE TABLE ALL_SONGS\
            (serial_number int PRIMARY KEY,\
            SongName varchar(100) NOT NULL,\
            ArtistName varchar(100),\
            SongPath varchar(150) NOT NULL)")
    _cursor.execute(
        "INSERT INTO ALL_SONGS\
        (serial_number,SongName,ArtistName,SongPath) \
            values({},'{}','{}',\'{}')".format(
                1,"Mortals","Warriyo","Mortals"))
    link.commit()
except: pass
_cursor.execute("USE SONGDB")
# ---------------------------------------------




#-------------ALL FUNCTIONS----------------------
def Play_Song():
    songIndex = SongBox.curselection()[0] + 1
    _cursor.execute(f"SELECT SongPath FROM ALL_SONGS\
        WHERE serial_number={songIndex}")
    for i in _cursor:
        print(i)
        mixer.music.load(f"songs\\{i[0]}.mp3")
        mixer.music.play()
        tkinter.Button(btnFrame,text="Pause",
            command=Pause_Song,width=8,
            relief="groove",pady=5,background='brown',
            font='arial 12 bold').grid(row=2,column=0)
        
def Resume_Song():
    mixer.music.unpause()
    tkinter.Button(btnFrame,text="Pause",
            command=Pause_Song,width=8,
            relief="groove",pady=5,background='brown',
            font='arial 12 bold').grid(row=2,column=0)
    
def Pause_Song():
    mixer.music.pause()
    tkinter.Button(btnFrame,text="Resume",
        command=Resume_Song,width=8,relief="groove",
        pady=5,background='brown',
        font='arial 12 bold').grid(row=2,column=0)
        
                

        
def add_song():
    
    def addsong():
        _cursor.execute("select count(*) from all_songs")
        songindex = 0
        for i in _cursor:
            songindex = int(i[0])+1
        if str(PathEntry.get()) in (" ",'',"  "):
            pass
        else:
            print(SnameEntry.get(),ArtistEntry.get(),
                  PathEntry.get())
            _cursor.execute("INSERT INTO ALL_SONGS\
                (serial_number,SongName,ArtistName,SongPath)\
                values({},'{}','{}','{}')".format(songindex,
                str(SnameEntry.get()),str(ArtistEntry.get()),
                str(PathEntry.get())))
            link.commit()
    
    root = tkinter.Tk()
    root.geometry('750x450')
    SnameVar = tkinter.StringVar()
    ArtistVar = tkinter.StringVar()
    SongPathVar = tkinter.StringVar()
    
    
    tkinter.Label(root,text='Enter Song Name: ',
            font='arial 15 bold').grid(row=1,column=1)
    SnameEntry = tkinter.Entry(root,
            textvariable=SnameVar,width=40)
    SnameEntry.grid(row=1,column=2,pady=15)
    
    tkinter.Label(root,text='Enter Artist Name: ',
            font='arial 15 bold').grid(row=2,column=1)
    ArtistEntry = tkinter.Entry(root,
            textvariable=ArtistVar,width=40)
    ArtistEntry.grid(row=2,column=2,pady=15)
    
    tkinter.Label(root,text='Enter Audio File Name(without extension): ',
                  font='arial 15 bold').grid(row=3,column=1)
    PathEntry = tkinter.Entry(root,textvariable=SongPathVar,width=40)
    PathEntry.grid(row=3,column=2,pady=15)
    
    tkinter.Button(root,text="Add",command=addsong,width=10,
                   font="arial 10 bold",pady=5,
                   relief='groove').grid(row=4,column=2,pady=60)
    
    
    root.mainloop()
  
 
    
def Delete():
    def confirm_delete():
        return tkmsg.askquestion("DELETE?",
            "Do you really want to delete this song??")
    if confirm_delete() == 'yes':
        songIndex = SongBox.curselection()[0] + 1
        _cursor.execute(f"DELETE FROM ALL_SONGS \
            WHERE serial_number = {songIndex}")
        link.commit()
        _cursor.execute(f"UPDATE ALL_SONGS \
            SET serial_number = serial_number-1\
            WHERE serial_number>{songIndex}")
        link.commit()
#------------------------------------------------------------------------

# Starting the mixer
mixer.init()

# Staring GUI Loop

root = tkinter.Tk()
root.config(background='brown')
root.geometry("1200x675")
root.minsize(1200,675)
root.title("Music Player")

#-----Space For Songs------
SongBox = tkinter.Listbox(root,width=100,
        height=20,background='black',foreground='white',
        font='arial 14 bold',cursor='dot')
SongBox.pack(pady=50)


_cursor.execute("SELECT SONGNAME,ArtistName FROM ALL_SONGS")
for s in _cursor:
    space = 100-len(s[0])
    SongBox.insert(tkinter.END,s[0]+' '*space+s[1])
    print(s[0])


#------------CREATING BUTTONS AND MENUS----------------
MainMenu = tkinter.Menu(root)
MainMenu.add_command(label="Add Song", command=add_song)
MainMenu.add_command(label="Delete", command=Delete)
root.config(menu=MainMenu)

btnFrame = tkinter.Frame(root,background='brown')
btnFrame.pack()
tkinter.Button(btnFrame,text="Play",command=Play_Song,
    width=15,pady=8,font="arial 12 bold",background='brown',
    foreground='black',relief="groove").grid(row=1,column=0,pady=5)


root.mainloop()