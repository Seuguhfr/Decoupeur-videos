import time
import keyboard

def write():
    # Récupérer le texte saisi par l'utilisateur
    text_to_type = "#AnimalAntics #FunnyFurballs #laugh #HilariousPets #hilariouspetstiktoktv #CuteAndFunny #smilesquad😝 #FurryFunnies #GiggleGang #krazychuckle #PetHumor #adorable #bell #youngzany #funnyfriends #therealquirkyone #AmusingAnimals #joyful #cutenessoverloaded🥰🥰🥰 #chort #guffadigang #cheerful #wildliferehab #grin"

    # Écrire le texte avec le clavier
    words = text_to_type.split()
    for word in words:
        keyboard.write(word)
        time.sleep(1+len(word)*0.01)  # Délai supplémentaire après chaque mot (ajustez si nécessaire)
        keyboard.press_and_release('enter')

if __name__ == "__main__":
    n = input("Combien de fois voulez-vous écrire le texte ? ")
    input("Appuyez sur Entrée pour commencer")
    time.sleep(5)
    for i in range(int(n)):
        write()
        keyboard.press_and_release('ctrl+tab')
        time.sleep(1)
    keyboard.press_and_release('ctrl+shift+tab')