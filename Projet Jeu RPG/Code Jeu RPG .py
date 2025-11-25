from tkinter import *
from PIL import Image, ImageTk
import os


#classe
class Race:
    def __init__(self, nom, bonus_stats, competences):
        self.nom = nom
        self.bonus_stats = bonus_stats
        self.competences = competences


class ClassePerso:
    def __init__(self, nom, bonus_stats, competences):
        self.nom = nom
        self.bonus_stats = bonus_stats
        self.competences = competences


class Personnage:
    def __init__(self, race, classe):
        self.race = race
        self.classe = classe
        self.stats = {"pv": 100, "force": 10, "vitesse": 5}
        self.appliquer_stats()
        self.competences_finales = []
        self.points_comp = 2


    def appliquer_stats(self):
        for s, v in self.race.bonus_stats.items():
            self.stats[s] += v
        for s, v in self.classe.bonus_stats.items():
            self.stats[s] += v


# Dictionnaire (plus simple pour recup l'objet genre Humain,ogre ect..)
races_list = {
    "Humain": Race("Humain", {"pv": 10, "force": 5, "vitesse": 5}, ["Diplomatie", "Courage", "Adaptabilité"]),
    "Ogre": Race("Ogre", {"pv": 40, "force": 15, "vitesse": -2}, ["Rage bestiale", "Peau épaisse", "Intimidation"]),
    "Elfe": Race("Elfe", {"pv": -5, "force": 3, "vitesse": 15}, ["Agilité elfique", "Vision nocturne", "Dextérité magique"]),
}


classes_list = {
    "Guerrier": ClassePerso("Guerrier", {"pv": 20, "force": 10, "vitesse": -1}, ["Frappe lourde", "Défense solide", "Provocation"]),
    "Archer": ClassePerso("Archer", {"pv": -5, "force": -2, "vitesse": 10}, ["Tir rapide", "Camouflage", "Vision précise"]),
    "Mage": ClassePerso("Mage", {"pv": -10, "force": 2, "vitesse": 3}, ["Boule de feu", "Bouclier magique", "Téléportation"]),
}

frame = Tk()
frame.title("RPG Ethan&Thibaud")
canvas = Canvas(frame, width=1400, height=900)
canvas.pack()

#bg et logo (peut etre resize le logo ou bouger ligne noir)
bg_img = ImageTk.PhotoImage(Image.open("image/fond.png"))
canvas.create_image(0, 0, anchor=NW, image=bg_img)
logo_img = ImageTk.PhotoImage(Image.open("image/logo.png").resize((200, 200)))
canvas.create_image(18, 20, anchor=NW, image=logo_img)


Frame(frame, bg="black", height=2, width=800).place(x=0, y=678)
Frame(frame, bg="black", height=2, width=800).place(x=800, y=600)
Frame(frame, bg="black", width=2, height=900).place(x=230, y=0)
Frame(frame, bg="black", width=2, height=900).place(x=800, y=0)

zone_texte = Text(frame, width=54, height=5, font=("Calisto MT", 14), bg="#EDC66A")
zone_texte.place(x=245, y=695)
zone_texte1 = Text(frame, width=57, height=9, font=("Calisto MT", 14), bg="#EDC66A")
zone_texte1.place(x=810, y=610)


# Fond pour image perso
image_label = Label(frame, bg="white")
canvas.create_window(250, 20, anchor=NW, window=image_label)


# Variables 
current_race = list(races_list.keys())[0]
current_classe = list(classes_list.keys())[0]
perso = Personnage(races_list[current_race], classes_list[current_classe])


# Fonctions gerer competence + update perso + affichage
def toggle_competence(comp):
    if comp in perso.competences_finales:
        perso.competences_finales.remove(comp)
        perso.points_comp += 1
    elif perso.points_comp > 0:
        perso.competences_finales.append(comp)
        perso.points_comp -= 1
    update_description()
    update_arbre()
#############################################################
#SOUCIS quand je switch de race ou classe
#si j'ai mis une competence dans la premiere de race 
#et que je change de race le points competence n'est pas redonner 
#il faut recliquer sur la race puis retirer la comp 
#############################################################
def update_description(event=None):
    global current_race, current_classe, perso
    if liste_race.curselection():
        current_race = liste_race.get(liste_race.curselection())
    if liste_classe.curselection():
        current_classe = liste_classe.get(liste_classe.curselection())


    # Conserver compétences et points
    old_comps = getattr(perso, "competences_finales", [])
    old_points = getattr(perso, "points_comp", 2)
    perso = Personnage(races_list[current_race], classes_list[current_classe])
    perso.competences_finales = old_comps
    perso.points_comp = old_points


    # Texte description
    texte = f"Race : {perso.race.nom}\nCompétences : {', '.join(perso.race.competences)}\n\n"
    texte += f"Classe : {perso.classe.nom}\nCompétences : {', '.join(perso.classe.competences)}"
    zone_texte.config(state="normal")
    zone_texte.delete("1.0", END)
    zone_texte.insert(END, texte)
    zone_texte.config(state="disabled")


    # Stats
    stats = perso.stats
    texte_stats = f"--- STATISTIQUES ---\nPV : {stats['pv']}\nForce : {stats['force']}\nVitesse : {stats['vitesse']}\nPoints Compétences : {perso.points_comp}"
    zone_texte1.config(state="normal")
    zone_texte1.delete("1.0", END)
    zone_texte1.insert(END, texte_stats)
    zone_texte1.config(state="disabled")


    # Image des perso
    key = f"{current_race}_{current_classe}"
    path = f"image/{key}.png"
    if os.path.exists(path):
        img = ImageTk.PhotoImage(Image.open(path).resize((530, 638)))
        image_label.config(image=img)
        image_label.image = img
    else:
        image_label.config(image="")
    update_arbre()
    update_listbox_colors()


def update_listbox_colors():
    # Race selectionner en vert
    for i in range(liste_race.size()):
        if liste_race.get(i) == current_race:
            liste_race.itemconfig(i, {'fg': 'green'})
        else:
            liste_race.itemconfig(i, {'fg': 'black'})
    # Classe selectionner en vert
    for i in range(liste_classe.size()):
        if liste_classe.get(i) == current_classe:
            liste_classe.itemconfig(i, {'fg': 'green'})
        else:
            liste_classe.itemconfig(i, {'fg': 'black'})


# arbre de competence
comp_frame = Frame(frame, bg="#EDC66A", bd=2, relief="ridge")
comp_frame.place(x=810, y=20, width=550, height=560)
Label(comp_frame, text="Arbre de Compétences", font=("Calisto MT", 24), bg="#EDC66A").pack(pady=10)


frame_race_comp = Frame(comp_frame, bg="#EDC66A")
frame_race_comp.pack(pady=10)
frame_classe_comp = Frame(comp_frame, bg="#EDC66A")
frame_classe_comp.pack(pady=10)


def update_arbre():
    for widget in frame_race_comp.winfo_children():
        widget.destroy()
    for widget in frame_classe_comp.winfo_children():
        widget.destroy()
    for i, comp in enumerate(perso.race.competences):
        color = "green" if comp in perso.competences_finales else "white"
        Button(frame_race_comp, text=comp, font=("Calisto MT", 14), width=15,
               bg=color, command=lambda c=comp: toggle_competence(c)).grid(row=0, column=i, padx=5)
    for i, comp in enumerate(perso.classe.competences):
        color = "green" if comp in perso.competences_finales else "white"
        Button(frame_classe_comp, text=comp, font=("Calisto MT", 14), width=15,
               bg=color, command=lambda c=comp: toggle_competence(c)).grid(row=0, column=i, padx=5)


# Liste box
Label(frame, text="Race :", font=("Calisto MT", 26), bg="#EDC66A").place(x=30, y=250)
liste_race = Listbox(frame, font=("Calisto MT", 20), height=3, width=12)
for race in races_list.keys():
    liste_race.insert(END, race)
liste_race.place(x=30, y=300)
liste_race.select_set(0)
liste_race.bind("<<ListboxSelect>>", update_description)


Label(frame, text="Classe :", font=("Calisto MT", 26), bg="#EDC66A").place(x=30, y=420)
liste_classe = Listbox(frame, font=("Calisto MT", 20), height=3, width=12)
for classe in classes_list.keys():
    liste_classe.insert(END, classe)
liste_classe.place(x=30, y=470)
liste_classe.select_set(0)
liste_classe.bind("<<ListboxSelect>>", update_description)


# popup recap final
def confirmer_personnage():
    popup = Toplevel(frame)
    popup.title("Récapitulatif du personnage")
    popup.geometry("500x400")
   
    Label(popup, text=f"Race : {perso.race.nom}", font=("Calisto MT", 18), fg="green").pack(pady=5)
    Label(popup, text=f"Classe : {perso.classe.nom}", font=("Calisto MT", 18), fg="green").pack(pady=5)
   
    stats = perso.stats
    stats_text = f"PV : {stats['pv']}\nForce : {stats['force']}\nVitesse : {stats['vitesse']}"
    Label(popup, text=stats_text, font=("Calisto MT", 16)).pack(pady=10)
   
    Label(popup, text="Compétences choisies :", font=("Calisto MT", 16)).pack(pady=5)
    for comp in perso.competences_finales:
        Label(popup, text=comp, font=("Calisto MT", 14), fg="green").pack()
   
   
#soucis décalage mettre x5 y750   
Button(frame, text="Confirmer Votre \n personnage", font=("Calisto MT", 20), bg="#EDC66A", command=confirmer_personnage).place(x=5, y=750)

update_description()
frame.resizable(False, False)
frame.mainloop()





