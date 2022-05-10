####### Projet QR code

# Librairies
import tkinter as tk
from tkinter import filedialog
import PIL as pil
from PIL import Image
from PIL import ImageTk 

# Constantes

# Variables globals
fichier = None

# Fonctions

def nbrCol(matrice):
    """
    renvoi le nombre de colonne d'une matrice
    """
    return len(matrice[0])

def nbrLig(matrice):
    """
    renvoie le nombre de ligne d'une matrice
    """
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

def charger(filename):
    global fichier, photo, picture_QR_code
    fichier = filename
    img = pil.Image.open(filename)
    photo = ImageTk.PhotoImage(img)  
    picture_QR_code.config(width = img.size[0], height = img.size[1])
    dessin = picture_QR_code.create_image(2,2,anchor = 'nw', image=photo)

def selection_fichier():
    """
    Affiche sur l'interface graphique le QR code à décoder
    """
    
    filename = filedialog.askopenfile(mode='rb', title='Choose a file')
    charger(filename)

def verif_taille(matrice):
    global QR_code_valide
    if nbrLig(matrice) != nbrCol(matrice):
        QR_code_valide = False

def rotate_droite(matrice):

    mat_rot=[[0]*nbrLig(matrice) for i in range(nbrCol(matrice))]

    for i in range(nbrLig(mat_rot)):
        for j in range(nbrCol(mat_rot)):
            mat_rot[i][j] = matrice[nbrLig(matrice)-1-j][i]
    
    return mat_rot

def rotate_gauche(matrice):
   
    mat_rot=[[0]*nbrLig(matrice) for i in range(nbrCol(matrice))]
    
    for i in range(nbrLig(mat_rot)):
        for j in range(nbrCol(mat_rot)):
            mat_rot[i][j] = matrice[j][nbrLig(matrice)-1-i]
    
    return mat_rot

def create_mat_coin():
    mat_coin = [[0,0,0,0,0,0,0,1]
                ,[0,1,1,1,1,1,0,1]
                ,[0,1,0,0,0,1,0,1]
                ,[0,1,0,0,0,1,0,1]
                ,[0,1,0,0,0,1,0,1]
                ,[0,1,1,1,1,1,0,1]
                ,[0,0,0,0,0,0,0,1]
                ,[1,1,1,1,1,1,1,1]]
    
    return mat_coin

def extraire_matrice(g_mat, p_mat):
    mat =[[0]*nbrLig(p_mat) for i in range(nbrCol(p_mat))]
    for i in range(nbrLig(p_mat)):
            for j in range(nbrCol(p_mat)):
                mat[i][j] = g_mat[i][j]
    return mat

def verif_sens_QR_code(mat):
    global coin_nw, coin_ne, coin_se, coin_sw
    global QR_code_valide

    mat_coin = create_mat_coin()
    
    coin_nw, coin_ne, coin_se, coin_sw = False, False, False, False

    mat2 = extraire_matrice(mat, mat_coin)

    if mat2 == mat_coin:
        coin_nw = True
        
    mat = rotate_gauche(mat)
    mat2 = extraire_matrice(mat, mat_coin)

    if mat2 == mat_coin:
        coin_ne = True
        
    mat = rotate_gauche(mat)
    mat2 = extraire_matrice(mat, mat_coin)

    if mat2 == mat_coin:
        coin_se = True
        
    mat = rotate_gauche(mat)
    mat2 = extraire_matrice(mat, mat_coin)
        
    if mat2 == mat_coin:
        coin_sw = True
    
    mat = rotate_gauche(mat)

    if coin_nw == True and coin_ne == False and coin_se == True and coin_sw == True:
        mat = rotate_droite(mat)
        
    elif coin_nw == True and coin_ne == True and coin_se == True and coin_sw == False:
        mat = rotate_gauche(mat)

    elif coin_nw == False and coin_ne == True and coin_se == True and coin_sw == True:
        mat = rotate_gauche(rotate_gauche(mat))
        
    elif coin_nw == True and coin_ne == True and coin_se == False and coin_sw == True:
        None
    
    else:
        QR_code_valide = False
    
    
    if QR_code_valide == True:
        saving(mat,"new.png")
        charger("new.png")
    
def verif_timing(matrice):
    timing = True
    mat_coin = create_mat_coin()
    pix = 0

    for i in range(nbrCol(mat_coin), nbrCol(matrice)-nbrCol(mat_coin)):
        
        if matrice[nbrLig(mat_coin)-2][i] == pix:

            if pix == 0:
                pix = 1
            else:
                pix = 0
                
        else:
            timing = False
            break

    return timing
    
def verif_all_timing(matrice):
    global QR_code_valide
    timing_top = verif_timing(matrice)
    timing_left = verif_timing(rotate_droite(matrice))
    if timing_top == True and timing_left == True:
        QR_code_valide = True
    else:
        QR_code_valide = False

def read(matrice):
    all_message = []
    for k in range(0,15,4):

        message_binaire = []
        for i in range(7):
            for j in range(2):
                message_binaire.append(matrice[(-1)-(j+k)][(-1)-i])
        all_message.append(message_binaire)
    
        message_binaire = []
        for i in range(7,14):
            for j in range(2):
                message_binaire.append(matrice[(-1)-(j+k)][(-1)-i])
        all_message.append(message_binaire)
    
        message_binaire = []
        for i in range(7):
            for j in range(2):
                message_binaire.append(matrice[(-1)-(j+k+2)][(-14)+i])
        all_message.append(message_binaire)

        message_binaire = []
        for i in range(7):
            for j in range(2):
                message_binaire.append(matrice[(-1)-(j+k+2)][(-7)+i])
        all_message.append(message_binaire)

    return(all_message)

def swap(bit_a_chg:int):
    swap = {0: 1, 1:0}
    swap[bit_a_chg]
    return bit_a_chg        
    
def code_hamming(message):
    final_message = []
    
    c1 = message[0]+ message[1], message[3]
    c2 = message[0]+ message[2], message[3]
    c3 = message[1]+ message[2], message[3]
    m1=message[0]
    m2=message[1]
    m3=message[2]
    m4=message[3]
    
  

    if c1!=message[4] and c2!=message[5] and c3==message[6]:
        message[0]=swap(message[0])

    if c1==message[4] and c2!=message[5] and c3!=message[6]:
        message[2]=swap(message[2])

    if c1!=message[4] and c2==message[5] and c3!=message[6]:
        message[1]=swap(message[1])

    if c1!=message[4] and c2!=message[5] and c3!=message[6]:
        message[3]=swap(message[3])

    final_message.append(message[0])
    final_message.append(message[1])
    final_message.append(message[2])
    final_message.append(message[3])
    return final_message

def determine_type_donnee(matrice):
    if matrice[24][8] == 0:
        type_donnee = "numérique"
    else:
        type_donnee = "brute"

    return type_donnee

def conversionEntier(liste,b):
    res = 0
    liste.reverse()
    for i in range(len(liste)):
        res += liste[i]*(b**i)
    return res

def conversionBase(nombre,b):
    if(nombre==0):
        return [0]
    res = []
    while nombre > 0:
        res.append(nombre%b)
        nombre //= b
    res.reverse()
    return res

def afficheBaseHexa(liste):
    for v in liste:
        if(v == 10):
            print('A',end="")
        elif(v == 11):
            print('B',end="")
        elif(v == 10):
            print('C',end="")
        elif(v == 11):
            print('D',end="")
        elif(v == 10):
            print('E',end="")
        elif(v == 11):
            print('F',end="")
        else:
            print(v, end="")

def dechiffrage_hexa(message):
    final_message = []
    print(final_message)

    print("hexa")

def dechiffrage_ASCII(message):
    message_final = []
    for i in range(0,nbrLig(message),2):
        message_final.append(message[i]+ message[i+1])
    print(message_final)
    for i in range(nbrLig(message_final)):
        message_final[i] = chr(conversionEntier(message_final[i],2))
    print("ASCII")
    print(message_final)
    return message_final

def dechiffrage_message(matrice,message):
    final_message = []
    
    for i in range(nbrLig(message)):
        final_message.append(message[i][:7])
        final_message.append(message[i][7:])

    
    for i in range(nbrLig(final_message)):
        final_message[i] = code_hamming(final_message[i])
    print(final_message)
    
    if determine_type_donnee(matrice) == "numérique":
        dechiffrage_hexa(final_message)                   
    else:
        dechiffrage_ASCII(final_message)

def decode():
    global QR_code_valide
    QR_code_valide = True    
    if fichier == None:
        None
    else:
        mat = loading(fichier)
        verif_taille(mat)
        if QR_code_valide == True:
            verif_sens_QR_code(mat)
            if QR_code_valide == True:
                mat = loading(fichier)
                verif_all_timing(mat)
                if QR_code_valide == True:
                    dechiffrage_message(mat,read(mat))
                     
                    
                        
        
        if QR_code_valide == False:
            print("QR code non valide") 



# Affichage graphique
main_windows = tk.Tk()
main_windows.title("Lecteur de QR Code")

picture_QR_code = tk.Canvas(main_windows, width=100, height=100, bg="red")
#message_QR_code = tk.Label(main_windows, text="t", bg="black", fg="white")

button_loading = tk.Button(main_windows, text="Charger", command = lambda : selection_fichier())
button_decode = tk.Button(main_windows, text="Décoder", command = lambda : decode())

picture_QR_code.grid(column=1, row=0)
#message_QR_code.grid(column=1, row=1)

button_loading.grid(column=0, row=0)
button_decode.grid(column=0, row=1)



main_windows.mainloop()
