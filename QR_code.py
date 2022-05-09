####### Projet QR code

# Librairies
import tkinter as tk
from tkinter import filedialog
import PIL as pil
from PIL import Image
from PIL import ImageTk 

# Constantes

# Variables globals
file = None

# Fonctions

def nbrCol(matrix):
    """
    renvoi le nombre de colonne d'une matrice
    """
    return len(matrix[0])


def nbrLig(matrix):
    """
    renvoie le nombre de ligne d'une matrice
    """
    return len(matrix)


def saving(matPix, filename):
    """
    Fonction qui sauvegarde l'image contenue dans matpix dans le fichier filename.
    Utiliser une extension png pour que la fonction fonctionne sans perte d'information.
    """
    
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)


def loading(filename):
    """
    Fonction qui charge le fichier image filename et renvoie une matrice de 0 et
     de 1 qui représente l'image en noir et blanc.
    """
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat


def open_file(filename):
    """
    Fonction qui affiche l'image chargée dans la fenêtre graphique.
    """
    global file, photo, picture_QR_code
    
    file = filename
    img = pil.Image.open(filename)
    photo = ImageTk.PhotoImage(img)  
    picture_QR_code.config(width = img.size[0], height = img.size[1])
    dessin = picture_QR_code.create_image(2,2,anchor = 'nw', image=photo)


def selection_file():
    """
    Fonction qui affiche sur l'interface graphique l'image sélectionnée.
    """
    
    filename = filedialog.askopenfile(mode='rb', title='Choose a file')
    open_file(filename)


def verification_size(matrix):
    """
    Fonction qui vérifie le nombre de lignes de la matrice est égal aux nombre de colonnes
    """
    global QR_code_valid
    
    if nbrLig(matrix) != nbrCol(matrix):
        QR_code_valid = False


def rotate_right(matrix):
    """
    Fonction qui renverse vers la droite la matrice et la retourne.
    """

    mat_rot=[[0]*nbrLig(matrix) for i in range(nbrCol(matrix))]

    for i in range(nbrLig(mat_rot)):
        for j in range(nbrCol(mat_rot)):
            mat_rot[i][j] = matrix[nbrLig(matrix)-1-j][i]
    
    return mat_rot


def rotate_left(matrix):
    """
    Fonction qui renverse vers la gauche la matrice et la retourne.
    """
   
    mat_rot=[[0]*nbrLig(matrix) for i in range(nbrCol(matrix))]
    
    for i in range(nbrLig(mat_rot)):
        for j in range(nbrCol(mat_rot)):
            mat_rot[i][j] = matrix[j][nbrLig(matrix)-1-i]
    
    return mat_rot


def create_matrix_corner():
    """
    Fonction qui crée et retourne une matrice corespondant aux coin spécifique des QR codes.
    """
    
    matrix_corner = [[0,0,0,0,0,0,0,1]
                ,[0,1,1,1,1,1,0,1]
                ,[0,1,0,0,0,1,0,1]
                ,[0,1,0,0,0,1,0,1]
                ,[0,1,0,0,0,1,0,1]
                ,[0,1,1,1,1,1,0,1]
                ,[0,0,0,0,0,0,0,1]
                ,[1,1,1,1,1,1,1,1]]
    
    return matrix_corner


def extract_matrix(big_matrix, small_matrix):
    """
    Fonction qui retourne un extrait de la matrice big_matrix,
     c'est extrait a les mêmes dimensions que la matrice small_matrix.
    """
    
    matrix =[[0]*nbrLig(small_matrix) for i in range(nbrCol(small_matrix))]
    
    for i in range(nbrLig(small_matrix)):
            for j in range(nbrCol(small_matrix)):
                matrix[i][j] = big_matrix[i][j]
    
    return matrix


def verification_orientation(matrix):
    """
    Fonction qui vérifie la présence des trois coins spécifiques aux QR code,
     et qui, si il y en a, oriente le QR code dans le bon sens si besoin.
    """
    global QR_code_valid

    matrix_corner = create_matrix_corner()
    
    # Création des variable corespondant aux quatre coins de la matrice.
    corner_nw, corner_ne, corner_se, corner_sw = False, False, False, False

    # On vérifie le coin nord-ouest de la matrice.
    matrix_2 = extract_matrix(matrix, matrix_corner)
    if matrix_2 == matrix_corner:
        corner_nw = True

    # On vérifie le coin nord-est de la matrice.    
    matrix = rotate_left(matrix)
    matrix_2 = extract_matrix(matrix, matrix_corner)
    if matrix_2 == matrix_corner:
        corner_ne = True

    # On vérifie le coin sud-est de la matrice.  
    matrix = rotate_left(matrix)
    matrix_2 = extract_matrix(matrix, matrix_corner)
    if matrix_2 == matrix_corner:
        corner_se = True

    # On vérifie le coin sud-ouest de la matrice.  
    matrix = rotate_left(matrix)
    matrix_2 = extract_matrix(matrix, matrix_corner)    
    if matrix_2 == matrix_corner:
        corner_sw = True
    
    matrix = rotate_left(matrix)

    # On réoriente ou non la matrice selon l'emplacement des coins.
    if corner_nw == True and corner_ne == False and corner_se == True and corner_sw == True:
        matrix = rotate_right(matrix)    
    elif corner_nw == True and corner_ne == True and corner_se == True and corner_sw == False:
        matrix = rotate_left(matrix)
    elif corner_nw == False and corner_ne == True and corner_se == True and corner_sw == True:
        matrix = rotate_left(rotate_left(matrix))   
    elif corner_nw == True and corner_ne == True and corner_se == False and corner_sw == True:
        None
    # Si il n'a pas le nombre de coin suffisant, le QR code n'est pas valide
    else:
        QR_code_valid = False
    
    # Si le QR code est valide on le sauvegarde dans un nouveau fichier
    if QR_code_valid == True:
        saving(matrix,"new.png")
        open_file("new.png")

  
def verif_timing(matrix):
    """
    Fonction qui retourne la présence ou non de timing.
    """
    
    timing = True
    mat_corner = create_matrix_corner()
    pixel = 0

    for i in range(nbrCol(mat_corner), nbrCol(matrix)-nbrCol(mat_corner)):    
        
        if matrix[nbrLig(mat_corner)-2][i] == pixel:
            if pixel == 0:
                pixel = 1
            else:
                pixel = 0
                
        else:
            timing = False
            break

    return timing


def verif_all_timing(matrix):
    """
    Fonction qui vérifie la présence et le bon placement des deux timings.
    """
    global QR_code_valid
    
    timing_top = verif_timing(matrix)
    timing_left = verif_timing(rotate_right(matrix))
    
    if timing_top == True and timing_left == True:
        QR_code_valid = True
    else:
        QR_code_valid = False


def read(matrix):
    """
    Fonction qui lie et retourne le code du message du QR code
    """
    
    code = []
    
    for k in range(0,15,4):
        
        # Lecture du bloc 1+k
        code_block = []
        for i in range(7):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k)][(-1)-i])
        code.append(code_block)
        
        # Lecture du bloc 2+k
        code_block = []
        for i in range(7,14):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k)][(-1)-i])
        code.append(code_block)
    
        # Lecture du bloc 3+k
        code_block = []
        for i in range(7):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k+2)][(-14)+i])
        code.append(code_block)

        # Lecture du bloc 4+k
        code_block = []
        for i in range(7):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k+2)][(-7)+i])
        code.append(code_block)

    return code


def code_hamming(liste):
    final_liste = None
    """
    c1 = liste[0]+ liste[1], liste[3]
    c2 = liste[0]+ liste[2], liste[3]
    c3 = liste[1]+ liste[2], liste[3]
    
    if c1 % 2 == 0:
        c1 = 0
    else:
        c1 = 1
    
    if c2 % 2 == 0:
        c2 = 0
    else:
        c2 = 1
    
    if c3 % 2 == 0:
        c3 = 0
    else:
        c3 = 1

    if c1 == 0 and c2 == 0 and c3 == 0:
        final_message = liste[:4]
    else:
        print("erreur")
    """
    final_liste = liste[:4]
    return final_liste


def determine_data(matrix):
    """
    Fonction qui retourne le type de donnée que contient la matrice.
    """
    
    if matrix[24][8] == 0:
        data = "numérique"
    else:
        data = "brute"

    return data


def conversion_integer(liste,base):
    """
    Fonction qui convertie et retourne, en entier de base 10, le nombre formée
     par les chiffres de la liste donné, dans n'importe quel base donné.
    """
    
    integer = 0
    for i in range(len(liste)):
        integer += liste[-i-1]*(base**i)
    return integer


def conversionBase(nombre,b):
    if(nombre==0):
        return [0]
    res = []
    while nombre > 0:
        res.append(nombre%b)
        nombre //= b
    res.reverse()
    return res
""" 
def afficheBaseHexa(liste):
    text = ""
    for v in liste:
        if(v == 10):
            text += "A"
        elif(v == 11):
            text += "B"
        elif(v == 12):
            text += "C"
        elif(v == 13):
            text += "D"
        elif(v == 14):
            text += "E"
        elif(v == 15):
            text += "F"
        else:
            text += str(v)
    print(text)
    return text
"""

def afficheBaseHexa(liste):
    for v in liste:
        #compléter le code
        if(v == 10):
            print('A',end="")
        elif(v == 11):
            print('B',end="")
        elif(v == 12):
            print('C',end="")
        elif(v == 13):
            print('D',end="")
        elif(v == 14):
            print('E',end="")
        elif(v == 15):
            print('F',end="")
        else:
            print(v, end="")   
    

def translate_hexa(matrix):
    """
    Fonction qui traduit et retourne en hexadécimal les données de la matrice.
    """
    for i in range(nbrLig(matrix)):
        matrix[i] = conversion_integer(matrix[i],2)
    print("tatatatat=\n",matrix)
    
    for i in range(nbrLig(matrix)):
        matrix[i] = afficheBaseHexa(matrix)
    #print("tatatatat=\n",message)

    return matrix


def translate_ASCII(matrix):
    """
    Fonction qui traduit et retourne en ASCII les données de la matrice.
    """
    
    message = []
    # Convertie la liste de listes de 4 bits en liste de listes de 8 bits.
    for i in range(0,nbrLig(matrix),2):
        message.append(matrix[i]+ matrix[i+1])
    
    # Convertie les 8 bits en symbole ASCII.
    for i in range(nbrLig(message)):
        message[i] = chr(conversion_integer(message[i],2))
    
    return message


def translate(matrix,code_matrix):
    """
    Fonction qui traduit et retourne le code du QR code.
    """
    
    code_2_matrix = []
    
    # Convertie la liste de listes de 14 bits en liste de listes de 7 bits.
    for i in range(nbrLig(code_matrix)):
        code_2_matrix.append(code_matrix[i][:7])
        code_2_matrix.append(code_matrix[i][7:])

    # Correction d'erreur du code.
    for i in range(nbrLig(code_2_matrix)):
        code_2_matrix[i] = code_hamming(code_2_matrix[i])
    
    # Détermine si les donnéé doivent être interpréter en hexadecimal ou en ASCII.
    if determine_data(matrix) == "numérique":
        code_2_matrix = translate_hexa(code_2_matrix)                   
    else:
        code_2_matrix = translate_ASCII(code_2_matrix)
    
    message = ""
    for i in code_2_matrix:
        message += str(i)

    print(message)
    return message


def decode():
    """
    Fonction qui appelle d'autre fonction nécessaire pour décoder le QR code
     et qui affiche le message obtenue dans la fenetre grapphique.
    """
    global QR_code_valid
    
    QR_code_valid = True    
    
    # Si il n'y a pas de fichier charger, rien ne se passe.
    if file == None:
        None
    
    # Si il y a un fichier charger...
    else:
        
        matrix_file = loading(file)
        
        # On vérifie que le fichier à bien les dimention d'un QR code.
        verification_size(matrix_file)
        
        if QR_code_valid == True:

            # On vérifie qu'il a les trois coins spécifiques des QR codes et si oui, on vérifie ensuite qu'il est dans le bon sens.
            verification_orientation(matrix_file)
            
            if QR_code_valid == True:
                
                matrix_file = loading(file)
                
                # On vérifie si dans le fichier les timings sont présent et bien placés.
                verif_all_timing(matrix_file)
                
                if QR_code_valid == True:
                    
                    # On déchiffre le message et on l'affiche dans la fenêtre graphique
                    texte = translate(matrix_file,read(matrix_file))
                    message_QR_code.config(text=texte)
        
        # Si le QR code n'est pas valide...
        if QR_code_valid == False:
            print("QR code non valide") 



# Affichage graphique
main_windows = tk.Tk()
main_windows.title("Lecteur de QR Code")

picture_QR_code = tk.Canvas(main_windows, width=100, height=100, bg="red")
message_QR_code = tk.Label(main_windows, text="t", bg="black", fg="white")

button_loading = tk.Button(main_windows, text="Charger", command = lambda : selection_file())
button_decode = tk.Button(main_windows, text="Décoder", command = lambda : decode())

picture_QR_code.grid(column=1, row=0)
message_QR_code.grid(column=1, row=1)

button_loading.grid(column=0, row=0)
button_decode.grid(column=0, row=1)



main_windows.mainloop()
