# ------------------------------------------------------------------------------------------------------------
#
#_____/\\\\\\\\\________/\\\\\\\\\\\______/\\\\\\\\\______________________/\\\\\\\\\______/\\\\\\\\\\\\\\\________/\\\\\\\\\_        
# ___/\\\\\\\\\\\\\____/\\\/////////\\\__/\\\///////\\\__________________/\\\///////\\\___\/\\\///////////______/\\\////////__       
#  __/\\\/////////\\\__\//\\\______\///__\/\\\_____\/\\\_________________\/\\\_____\/\\\___\/\\\_______________/\\\/___________      
#   _\/\\\_______\/\\\___\////\\\_________\/\\\\\\\\\\\/_____/\\\\\\\\\\\_\/\\\\\\\\\\\/____\/\\\\\\\\\\\______/\\\_____________     
#    _\/\\\\\\\\\\\\\\\______\////\\\______\/\\\//////\\\____\///////////__\/\\\//////\\\____\/\\\///////______\/\\\_____________    
#     _\/\\\/////////\\\_________\////\\\___\/\\\____\//\\\_________________\/\\\____\//\\\___\/\\\_____________\//\\\____________   
#      _\/\\\_______\/\\\__/\\\______\//\\\__\/\\\_____\//\\\________________\/\\\_____\//\\\__\/\\\______________\///\\\__________  
#       _\/\\\_______\/\\\_\///\\\\\\\\\\\/___\/\\\______\//\\\_______________\/\\\______\//\\\_\/\\\\\\\\\\\\\\\____\////\\\\\\\\\_ 
#        _\///________\///____\///////////_____\///________\///________________\///________\///__\///////////////________\/////////__
#
# ------------------------------------------------------------------------------------------------------------
# Welcome to ASR-REC Speech to text | @ECAM-EPMI 2023 by CAprogs
# This is an end to end project that aims to use a pretrained neural network for voice recognition (Speech to text).
# The model used is the "Google Speech Recognition". / ( more model to come )
# Internet access is required to use this software.
# Audio files are deleted after every session.
# 3 Languages ​​are available: French, English, Arabic (Morocco) [ https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages?hl=en ]
# Credits: @Tkinter Designer by ParthJadhav
# ------------------------------------------------------------------------------------------------------------

# Update ( create a Json.config file to control the : deletion of the file after every session, model used )

# Importation des bibliothèques
from pathlib import Path
from tkinter import filedialog
import sounddevice as sd
import soundfile as sf
from tkinter import Tk,PhotoImage,Button,Canvas,StringVar,OptionMenu
from tkinter import messagebox
import speech_recognition as sr
import pygame
import os
import shutil

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# chemin relatif vers le dossier "assets/frame0"
assets_directory = script_directory / "frame0"

# chemin relatif vers le dossier "User_audio"
folder_path = script_directory / "User_audio"

# Créer le dossier
os.makedirs(folder_path)

i = 0  # Gestion du nombre d'enregistrements
record_duration = 10 # Durée d'enregistrement en secondes
Listen_state = True  # État du bouton Listen au 1er click
Listen_state2 = True # État2 du bouton Listen au 1er click
audio_paused = False # Etat de l'audio 
file_path_global = "No file available" # Indicateur du chemin audio en cours
Files_deleted_state = False # Etat des fichiers à la fermeture de l'application

# Initialiser l'objet Recognizer
r = sr.Recognizer()

# Initialiser la fenêtre Tkinter
window = Tk()

# Initialisation de Pygame pour la lecture audio
pygame.init()

###################################################################### Fonctions
# Importation des éléments graphique
def relative_to_assets(path: str) -> Path:
    return assets_directory / Path(path)

# Supprimer les fichiers à la fermeture de l'application
def delete_folder(folder_path):
    global Files_deleted_state
    #Fermer tous les processus audio en cours
    pygame.mixer.music.stop()
    pygame.quit()
    # Supprimer le dossier complet
    shutil.rmtree(folder_path)
    Files_deleted_state = True

# Fonction associée à la fermeture de l'application
def on_closing():
    global folder_path
    global Files_deleted_state
    delete_folder(folder_path)
    if Files_deleted_state:
        # Affichage d'un message de confirmation
        messagebox.showinfo("Fermeture", "Les fichiers audio ont été supprimés.")
    # Fermeture de la fenêtre tkinter
    window.destroy()

def Listen_enter(event):
    global Listen_state
    if Listen_state:
        button_3.configure(image=button_image_33)
    else:
        button_3.configure(image=button_image_4)

def Listen_leave(event):
    global Listen_state
    if Listen_state:
        button_3.configure(image=button_image_3)
    else:
        button_3.configure(image=button_image_44)

def Record_enter(event):
    button_1.configure(image=button_image_11)

def Record_leave(event):
    button_1.configure(image=button_image_1)

def Import_enter(event):
    button_2.configure(image=button_image_22)

def Import_leave(event):
    button_2.configure(image=button_image_2)

# Lorsque le bouton Listen est cliqué
def Listen_clicked(event):
    global Listen_state
    global Listen_state2
    global file_path_global
    global audio_paused
    if Listen_state2:
        button_3.configure(image=button_image_4)
        if file_path_global != "No file available" and not pygame.mixer.music.get_busy() and audio_paused == False:
            Listen_state = False
            Listen_state2 = False
            # Charger le fichier audio
            pygame.mixer.music.load(file_path_global)
            # Jouer le fichier audio
            pygame.mixer.music.play()
        elif file_path_global != "No file available" and not pygame.mixer.music.get_busy() and audio_paused == True:
            Listen_state = False
            Listen_state2 = False
            # Reprendre la lecture
            pygame.mixer.music.unpause()
            audio_paused = False
        else:
            pass
    else:
        if file_path_global != "No file available" and pygame.mixer.music.get_busy() and audio_paused == False:
            button_3.configure(image=button_image_33)
            Listen_state2 = True
            Listen_state = True
            # Mettre en pause la lecture
            pygame.mixer.music.pause()
            audio_paused = True
        else:
            pass

# Fonction qui gère l'appuie du bouton pour écouter l'audio enregistré ou importé  
def Listen():
    global Listen_state2
    global Listen_state
    global audio_paused
    global file_path_global
    if not audio_paused and not pygame.mixer.music.get_busy() and file_path_global != "No file available":
        Listen_state2 = True
        Listen_state = True
        audio_paused = False
    else:
        pass

# Gérer l'action du bouton d'enregistrement de la voix
def record_voice():
    global i
    global file_path_global
    global record_duration
    global folder_path

    duration = record_duration  # Durée de l'enregistrement en secondes
    fs = 44100  # Fréquence d'échantillonnage

    audio_file_path = folder_path / f"{i}.wav"
    audio_file_path = str(audio_file_path)
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    file_path_global = audio_file_path
    sd.wait() # Attendre la fin de l'enregistrement
    sf.write(audio_file_path, recording, fs)
    
    canvas.itemconfig(Path_listen, text=f"{os.path.basename(os.path.dirname(audio_file_path))+'/'+os.path.basename(audio_file_path)}")
    traduction = SpeechToText(audio_file_path)
    canvas.itemconfig(traduction_area, text=f"{traduction}")
    i += 1

# Gérer l'action du bouton d'importation d'un fichier audio
def import_audio():
    global file_path_global
    file_path = filedialog.askopenfilename()
    if file_path:
        traduction = SpeechToText(file_path)
        canvas.itemconfig(traduction_area, text=f"{traduction}")
        canvas.itemconfig(Path_listen, text=f"{os.path.basename(os.path.dirname(file_path))+'/'+os.path.basename(file_path)}")
        file_path_global = file_path
    else:
        pass

# Fonction de Traduction de l'audio 
def SpeechToText(filepath):
    with sr.AudioFile(filepath) as source:
        audio = r.record(source)  # Lire l'audio en entier

    language=language_var.get()
    # Associe la traduction du modèle à la langue définie
    if language == "English":
        language ="en-US"
        try:
            traduction = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            traduction = "Error : ASR-REC could not understand audio"
        except sr.RequestError:
            traduction = "RequestError : ASR-REC could not reach Google Server"
    elif language == "Arabic":
        language ="ar-MA"
        try:
            traduction = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            traduction = "خطأ: تعذر على نظام التعرف التلقائي على الكلام فهم الصوت."
        except sr.RequestError:
            traduction = "خطأ في الطلب: تعذر على نظام التعرف التلقائي على الكلام الوصول إلى خادم Google."
    elif language == "French":
        language ="fr-FR"
        try:
            traduction = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            traduction = "Error : ASR-REC n'a pas pu comprendre l'audio"
        except sr.RequestError:
            traduction = "RequestError : ASR-REC could not reach Google Server"
            
    return traduction
######################################################################

window.title("Automatic Speech Recognition - ECAM PROJECT")

window.geometry("962x686")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=686,
    width=962,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    480.0,
    208.0,
    image=image_image_1
)

# Liste déroulante pour le choix de la langue
language_var = StringVar(window)
language_var.set("French")  # Valeur par défaut

# Langues par défaut ( possibilité d'ajouter d'autres langues )
language_dropdown = OptionMenu(
    window,
    language_var,
    "French",
    "English",
    "Arabic"
)

language_dropdown.configure(
    bg="#FFFFFF"
)  

# Calculer les coordonnées X et Y pour centrer la liste déroulante
window_width = 962
window_height = 686
dropdown_width = 217
dropdown_height = 51
dropdown_x = (window_width - dropdown_width) / 2
dropdown_y = (window_height - dropdown_height) / 2

language_dropdown.place(
    x=dropdown_x,
    y=dropdown_y,
    width=dropdown_width,
    height=dropdown_height
)

canvas.create_rectangle(
    346.0,
    414.0,
    349.0,
    568.0,
    fill="#000000",
    outline="")

canvas.create_text(
    360.0,
    667.0,
    anchor="nw",
    text="ECAM-EPMI engineering project @2023",
    fill="#000000",
    font=("Mate Regular", 10 * -1)
)
##############################################################################################
###############################################                                                       Button Record
button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=record_voice,
    relief="flat",
    cursor="hand2"
)
button_1.place(
    x=97.0,
    y=506.0,
    width=221.0,
    height=51.0
)
button_1.bind("<Enter>", Record_enter)  # Lorsque la souris entre dans la zone du bouton
button_1.bind("<Leave>", Record_leave)   # Lorsque la souris quitte la zone du bouton

###############################################                                                       Button Import File
button_image_22 = PhotoImage(file=relative_to_assets("button_22.png"))
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=import_audio,
    relief="flat",
    cursor="hand2"
)
button_2.place(
    x=97.0,
    y=425.0,
    width=221.0,
    height=51.0
)

button_2.bind("<Enter>", Import_enter)  # Lorsque la souris entre dans la zone du bouton
button_2.bind("<Leave>", Import_leave)   # Lorsque la souris quitte la zone du bouton

###############################################                                                         Button Listen
button_image_44 = PhotoImage(file=relative_to_assets("button_44.png"))
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_image_33 = PhotoImage(file=relative_to_assets("button_33.png"))
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=Listen,
    relief="flat",
    cursor="hand2"
)
button_3.place(
    x=397.0,
    y=586.0,
    width=53.0,
    height=53.0
)

button_3.bind("<ButtonPress>", Listen_clicked) # Lier à la fonction Listen_clicked
button_3.bind("<Enter>", Listen_enter)  # Lorsque la souris entre dans la zone du bouton
button_3.bind("<Leave>", Listen_leave)   # Lorsque la souris quitte la zone du bouton
##############################################################################################

image_image_3 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_3 = canvas.create_image(
    647.0,
    498.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    678.0,
    613.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_5 = canvas.create_image(
    205.0,
    579.9999771118164,
    image=image_image_5
)

canvas.create_text(
     385.0,
     402.0,
     anchor="nw",
     text="     Text :",
     fill="#000000",
     font=("Inter", 16 * -1)
 )

###############################################                                                         Sortie de traduction
text = "..."
text_width = 480  # Largeur maximale pour le texte avant qu'il ne se répartisse sur plusieurs lignes
traduction_area = canvas.create_text(
    412.0,
    438.0,
    anchor="nw",
    text=text,
    fill="#000000",
    font=("Inter", 14 * -1),
    width=text_width
)
###############################################

Affiche_decompteur = canvas.create_text(
    184.0,
    574.0068359375,
    anchor="nw",
    text=f" 00 : {record_duration}",
    fill="#000000",
    font=("Inter Bold", 11 * -1)
)

Path_listen = canvas.create_text(
    472.0,
    607.0,
    anchor="nw",
    text=file_path_global,
    fill="#000000",
    font=("Inter", 11 * -1)
)

# Définition de l'action à effectuer lors de la fermeture
window.protocol("WM_DELETE_WINDOW", on_closing)

# Empêcher le redimensionnement de la fenêtre
window.resizable(False, False)
window.mainloop()