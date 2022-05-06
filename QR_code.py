###### Projet QR code

# Librairies
import tkinter as tk
from tkinter import filedialog
import PIL as pil
from PIL import Image
from PIL import ImageTk 

# Constantes

# Variables globals



# Fonctions

def nbrCol(matrice):
    return len(matrice[0])

def nbrLig(matrice):
    return len(matrice)

def saving(matPix, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat

def charger():
    global filename, photo, picture_QR_code
    filename = filedialog.askopenfile(mode='rb', title='Choose a file')
    img = pil.Image.open(filename)
    photo = ImageTk.PhotoImage(img)  
    picture_QR_code.config(width = img.size[0], height = img.size[1])
    dessin = picture_QR_code.create_image(2,2,anchor = 'nw', image=photo)
    

def decode(filename):
    mat = loading(filename)
    print(mat)


# Affichage graphique
main_windows = tk.Tk()
main_windows.title("Lecteur de QR Code")

picture_QR_code = tk.Canvas(main_windows, width=100, height=100, bg="red")
#message_QR_code = tk.Label(main_windows, text="t", bg="black", fg="white")

button_loading = tk.Button(main_windows, text="Charger", command = lambda : charger())
button_decode = tk.Button(main_windows, text="Décoder", command = lambda : decode("frame.png"))

picture_QR_code.grid(column=1, row=0)
#message_QR_code.grid(column=1, row=1)

button_loading.grid(column=0, row=0)
button_decode.grid(column=0, row=1)



main_windows.mainloop()