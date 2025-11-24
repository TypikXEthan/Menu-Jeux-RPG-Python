from tkinter import *
from PIL import Image, ImageTk
import os

# --------- Fenêtre principale ---------
frame = Tk()
frame.title("Menu Jeu")
frame.geometry("1400x900")

# --------- Canvas pour fond et logo ---------
canvas = Canvas(frame, width=1400, height=900)
canvas.pack()

bg_img = ImageTk.PhotoImage(Image.open("image/fond.png"))
canvas.create_image(0, 0, anchor=NW, image=bg_img)

logo_img = ImageTk.PhotoImage(Image.open("image/logo.png").resize((200, 200)))
canvas.create_image(18, 20, anchor=NW, image=logo_img)

# --------- Lignes de séparation ---------
longueur_ligne = 800
ligne = Frame(frame, bg="black", height=2, width=longueur_ligne)
ligne.place(x=0, y=678)

ligne1 = Frame(frame, bg="black", height=2, width=longueur_ligne)
ligne1.place(x=800, y=600)

ligne_v = Frame(frame, bg="black", width=2)
ligne_v.place(x=230, y=0, relheight=1)

ligne_v1 = Frame(frame, bg="black", width=2)
ligne_v1.place(x=800, y=0, relheight=1)

# --------- Boutons ---------
btn1 = Button(frame, text="Jouer", font=("Calisto MT", 48), fg="black", bg= "#EDC66A", borderwidth=0)
btn1.place(x=15, y=688)

btn2 = Button(frame, text="Confirmer", font=("Calisto MT", 20), fg="black", bg= "#EDC66A" , borderwidth=0)
btn2.place(x=50, y=600)

# --------- Zone description ---------
zone_texte = Text(frame, width=54, height=5, font=("Calisto MT", 14), bg="#EDC66A", fg="black", bd=2)
zone_texte.place(x=245, y=695)
zone_texte.insert(END, "Sélectionnez une race et une classe pour voir la description.")
zone_texte.config(state="disabled")

# --------- Zone des stats ---------
zone_texte1 = Text(frame, width=57, height=9, font=("Calisto MT", 14), bg="#EDC66A", fg="black", bd=2)
zone_texte1.place(x=810, y=610)
zone_texte1.insert(END, "Sélectionnez une race et une classe pour voir les statistiques.")
zone_texte1.config(state="disabled")

# --------- Descriptions ---------
descriptions_race = {
    "humain": "Les Humains sont adaptables et équilibrés.",
    "elfe": "Les Elfes sont agiles et précis.",
    "ogre": "Les Ogres sont puissants mais peu agiles."
}

descriptions_classe = {
    "guerrier": "Le Guerrier excelle au corps à corps.",
    "mage": "Le Mage maîtrise des sorts destructeurs.",
    "archer": "L'Archer attaque avec précision à distance."
}

# --------- Statistiques ---------
stats_race = {
    "humain": {"FOR": 45, "AGI": 30, "INT": 50, "PV": 50},
    "elfe": {"FOR": 25, "AGI": 50, "INT": 60, "PV": 30},
    "ogre": {"FOR": 55, "AGI": 10, "INT": 20, "PV": 60}
}

stats_classe = {
    "guerrier": {"FOR": 25, "AGI": 20, "INT": 10, "PV": 30},
    "mage": {"FOR": 0, "AGI": 15, "INT": 60, "PV": 5},
    "archer": {"FOR": 10, "AGI": 30, "INT": 20, "PV": 15}
}

# --------- Listes ---------
races = ["humain", "elfe", "ogre"]
classes = ["guerrier", "mage", "archer"]

# --------- Images ---------
images_combinaison = {}
for race in races:
    for classe in classes:
        path = f"image/{race}_{classe}.png"
        key = f"{race}_{classe}"
        if os.path.exists(path):
            images_combinaison[key] = ImageTk.PhotoImage(Image.open(path).resize((530, 638)))
        else:
            images_combinaison[key] = None
            print("Image manquante :", path)

image_label = Label(frame, bg="white")
canvas.create_window(250, 20, anchor=NW, window=image_label)

# --------- Variables ---------
current_race = races[0]
current_classe = classes[0]


# --------- Fonction de mise à jour ---------
def update_description():
    global current_race, current_classe

    if liste_race.curselection():
        current_race = liste_race.get(liste_race.curselection())

    if liste_classe.curselection():
        current_classe = liste_classe.get(liste_classe.curselection())

    # ---- TEXTE ----
    texte = (
        f"Race : {current_race}\n{descriptions_race[current_race]}\n\n"
        f"Classe : {current_classe}\n{descriptions_classe[current_classe]}"
    )

    zone_texte.config(state="normal")
    zone_texte.delete("1.0", END)
    zone_texte.insert(END, texte)
    zone_texte.config(state="disabled")

    # ---- CALCUL DES STATS ----
    stats_finales = {}

    for stat in ["FOR", "AGI", "INT", "PV"]:
        base = stats_classe[current_classe][stat]
        bonus_race = stats_race[current_race][stat]

        if bonus_race < 0:
            bonus_race = 0

        total = base + bonus_race
        if total > 100:
            total = 100

        stats_finales[stat] = total

    # ---- AFFICHAGE STATS ----
    texte_stats = (
        f"--- STATISTIQUES ---\n"
        f"FOR : {stats_finales['FOR']}\n"
        f"AGI : {stats_finales['AGI']}\n"
        f"INT : {stats_finales['INT']}\n"
        f"PV  : {stats_finales['PV']}"
    )

    zone_texte1.config(state="normal")
    zone_texte1.delete("1.0", END)
    zone_texte1.insert(END, texte_stats)
    zone_texte1.config(state="disabled")

    # ---- IMAGE ----
    key = f"{current_race}_{current_classe}"
    if images_combinaison[key]:
        image_label.config(image=images_combinaison[key])
        image_label.image = images_combinaison[key]
    else:
        image_label.config(image="")


# --------- Menu Race ---------
Label_race = Label(frame, text="Race :", font=("Calisto MT", 26), bg="#EDC66A")
canvas.create_window(30, 250, anchor=NW, window=Label_race)

liste_race = Listbox(canvas, font=("Calisto MT", 20), height=3, width=12)
for race in races:
    liste_race.insert(END, race)
canvas.create_window(30, 300, anchor=NW, window=liste_race)
liste_race.select_set(0)
liste_race.bind("<<ListboxSelect>>", lambda e: update_description())

# --------- Menu Classe ---------
Label_classe = Label(frame, text="Classe :", font=("Calisto MT", 26), bg="#EDC66A")
canvas.create_window(30, 420, anchor=NW, window=Label_classe)

liste_classe = Listbox(canvas, font=("Calisto MT", 20), height=3, width=12)
for classe in classes:
    liste_classe.insert(END, classe)
canvas.create_window(30, 470, anchor=NW, window=liste_classe)
liste_classe.select_set(0)
liste_classe.bind("<<ListboxSelect>>", lambda e: update_description())

# --------- Mise à jour initiale ---------
update_description()


# =============================================
#             ARBRE DE COMPÉTENCES
# =============================================
skill_frame = Frame(frame, bg="#EDC66A", bd=2, relief="ridge")
skill_frame.place(x=810, y=20, width=550, height=560)

titre_skill = Label(skill_frame, text="Arbre de Compétences", font=("Calisto MT", 24), bg="#EDC66A")
titre_skill.pack(pady=10)

# --- Sous-partie : Race ---
titre_race_skill = Label(skill_frame, text="Compétences de Race", font=("Calisto MT", 20), bg="#EDC66A")
titre_race_skill.pack()

frame_race_skill = Frame(skill_frame, bg="#EDC66A")
frame_race_skill.pack(pady=10)

btn_race1 = Button(frame_race_skill, text="Force+", font=("Calisto MT", 14), width=12)
btn_race1.grid(row=0, column=0, padx=10)

btn_race2 = Button(frame_race_skill, text="Agilité+", font=("Calisto MT", 14), width=12)
btn_race2.grid(row=0, column=1, padx=10)

btn_race3 = Button(frame_race_skill, text="Intelligence+", font=("Calisto MT", 14), width=12)
btn_race3.grid(row=0, column=2, padx=10)

Frame(skill_frame, bg="black", height=2).pack(fill="x", pady=15)

# --- Sous-partie : Classe ---
titre_classe_skill = Label(skill_frame, text="Compétences de Classe", font=("Calisto MT", 20), bg="#EDC66A")
titre_classe_skill.pack()

frame_classe_skill = Frame(skill_frame, bg="#EDC66A")
frame_classe_skill.pack(pady=10)

btn_classe1 = Button(frame_classe_skill, text="Attaque spé", font=("Calisto MT", 14), width=12)
btn_classe1.grid(row=0, column=0, padx=10)

btn_classe2 = Button(frame_classe_skill, text="Défense spé", font=("Calisto MT", 14), width=12)
btn_classe2.grid(row=0, column=1, padx=10)

btn_classe3 = Button(frame_classe_skill, text="Ultime", font=("Calisto MT", 14), width=12)
btn_classe3.grid(row=0, column=2, padx=10)


# --------- Mainloop ---------
frame.resizable(False, False)
frame.mainloop()
