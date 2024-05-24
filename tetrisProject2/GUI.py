from tkinter import *
from musictetris import *


        
def play():
    window.destroy()
    play_music('C:\\Users\\Basem Magdy\\Downloads\\Tetris Remix.mp3',)
def Exit():
    window.destroy()
    wait_for_input




    

window = Tk()
button_play= Button(window,text='Play',command=play,font=('Calibri',40,'italic'),fg='Yellow',bg='#000435',relief=RAISED,activebackground='Grey',activeforeground='Yellow',bd=10)
button_play.pack(side=LEFT)
button_exit=Button(window,text='Exit',command=Exit,font=('Calibri',40,'italic'),fg='Yellow',bg='#000435',relief=RAISED,activebackground='Red',activeforeground='Yellow',bd=10)
button_exit.pack(side=RIGHT)

window.geometry('1920x1080')
window.title('Tetris')
photo = PhotoImage(file='NEWTETRISICON.png')
photo2 = PhotoImage(file='TEAM NAMESwhiteversion.png')
label = Label(window,image=photo,font = ('Calibri',40,'italic'),fg='Black', bg= '#000435', relief=RAISED, bd=10, padx = 20, pady = 20)
label.pack()
label2 =Label(window,image=photo2,font =('Calibri',40,'italic'),fg='Black', bg='#000435')
label2.pack()










window.configure(bg='#000435')






window.mainloop()