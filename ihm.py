from tkinter import *

frame = Tk()
frame.title("menu jeu")
frame.geometry("600x600")

# Charger l'image
background = PhotoImage(file="image/fond.png")


# Label qui contient l'image
label_bg = Label(frame, image=background)
label_bg.place(x=0, y=0, relwidth=1, relheight=1)

frame.mainloop()
