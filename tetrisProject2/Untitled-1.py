from musictetris import *
from customtkinter import *
from tkinter import PhotoImage
import os
def play():
    play_music('Tetris Remix.mp3')
    window.destroy()
    os.system("project.py")
def Exit():
    window.destroy()
    stop_music()

def about_us():
    import about_us


window = CTk()
window.geometry('900x700')
window.title('Tetris')
window._set_appearance_mode("dark")

frame = CTkFrame(master=window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

button_play = CTkButton(frame, text='Play', command=play, font=('Arial', 40, 'italic'), width=150, height=100, corner_radius=10, fg_color="dark blue",)
button_play.place(x=330, y=330)

button_exit = CTkButton(frame, text='Exit', command=Exit, font=('Arial', 40, 'italic'), fg_color="dark blue", width=150, height=100, corner_radius=10 )
button_exit.place(x=330, y=450)

about_us_button = CTkButton(frame, text="about us", command=about_us, font=('Arial', 40, 'italic'),  fg_color="dark blue", width=150, height=100, corner_radius=10)
about_us_button.place(x=320, y=200)

photo = PhotoImage(file=r'TETRIS.ICON2.png')

label = CTkLabel(frame, text="", image=photo, font=('Arial', 40, 'italic'), fg_color='transparent', compound="center")
label.place(x=110, y=30)


window.mainloop()
