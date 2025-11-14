class Races(object):
    def _init_(self):
        self.nom ="nom"

class classe(object):
    def _init_(self):
        self.nom ="nom"

print("Choix de la race ")
print("1 Ogre")
print("2 Elfe")
print("3 Humain")
choix_race = input("Choix : ")

if choix_race == "1":
    race = Races("Ogre")
elif choix_race == "2":
    race = Races("Elfe")
elif choix_race == "3":
    race = Races("Humain")
else:
    race = Races("Inconnue")


print("Choix class")
print("1 Guerrier")
print("2 Archer")
print("2 Mage")
choix_classe = input("Choix : ")

if choix_classe == "1":
    race = classe("Geurrier") 
elif choix_classe == "2":
    race = classe("archer")
elif choix_classe == "3":
    race = classe("Mage")
else:
    race = classe("Inconnue")
