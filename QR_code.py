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


def create_filter(matrix):
    """
    Fonction qui créés et retourne un filtre selon le type de filtre indiquée par le QR code.
    """

    code = [matrix[22][8]] + [matrix[23][8]]

    matrix_filter = [[0]*nbrCol(matrix) for i in range(nbrLig(matrix))]

    if code == [0,0]:
        None
    
    # Créé un damier don le pixel tous en haut à gauche est noire.
    elif code == [0,1]:
        pixel = 0
        for i in range(nbrLig(matrix)):
            for j in range(nbrCol(matrix)):
                matrix_filter[i][j] = pixel
                if pixel == 0:
                    pixel = 1
                else:
                    pixel = 0
            if matrix_filter[i][0] == 0:
                    pixel = 1
            else:
                pixel = 0
    
    # Crée une matrice dont les lignes horizontales alternent entre noires et blancs, la plus haute est noire.
    elif code == [1,0]:
        pixel = 0
        for i in range(nbrLig(matrix)):
            for j in range(nbrCol(matrix)):
                matrix_filter[i][j] = pixel
            if pixel == 0:
                pixel = 1
            else:
                pixel = 0
    
    # Créé une matrice dont les lignes verticales alternent entre noires et blancs, la plus à gauche est noire.
    elif code == [1,1]:
        pixel = 0
        for i in range(nbrLig(matrix)):
            for j in range(nbrCol(matrix)):
                matrix_filter[i][j] = pixel
                if pixel == 0:
                    pixel = 1
                else:
                    pixel = 0
            if matrix_filter[i][0] == 0:
                    pixel = 0
            else:
                pixel = 1
    
    return matrix_filter


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

    #create_filter(matrix)
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


def number_block_read(matrix):
    """
    Fonction qui determine combien de bloc il faut lire dans le QR code"""
    
    number_block = []
    for i in range(13,18):
        number_block.append(matrix[i][0])
    
    number_block = conversion_integer(number_block,2)
    
    return number_block


def read(matrix):
    """
    Fonction qui lie et retourne le code du message du QR code
    """
    
    number_block = number_block_read(matrix)
    code = []
    
    for k in range(0,15,4):
        
        # Lecture du bloc 1+k
        code_block = []
        for i in range(7):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k)][(-1)-i])
        code.append(code_block)
        
        if 1+k == number_block:
            break

        # Lecture du bloc 2+k
        code_block = []
        for i in range(7,14):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k)][(-1)-i])
        code.append(code_block)

        if 2+k == number_block:
            break
        
        # Lecture du bloc 3+k
        code_block = []
        for i in range(7):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k+2)][(-14)+i])
        code.append(code_block)

        if 3+k == number_block:
            break

        # Lecture du bloc 4+k
        code_block = []
        for i in range(7):
            for j in range(2):
                code_block.append(matrix[(-1)-(j+k+2)][(-7)+i])
        code.append(code_block)

        if 4+k == number_block:
            break
    
    return code


def swap(bit_a_chg):
    """
    Fonction qui echange les 0 et les 1
    """
    if bit_a_chg == 1:
        bit_a_chg = 0
    else:
        bit_a_chg = 1
    return bit_a_chg        
    
def code_hamming(message):
    """
    Fonction qui sort 4 bits corriger
    """

    final_message = []
    
    c1 = (message[0]+ message[1] +message[3])%2
    c2 = (message[0]+ message[2]+ message[3])%2
    c3 = (message[1]+ message[2]+message[3])%2
    m1=message[0]
    m2=message[1]
    m3=message[2]
    m4=message[3]
    

    if c1!=message[4] and c2!=message[5] and c3==message[6]:
        m1=swap(m1)


    if c1==message[4] and c2!=message[5] and c3!=message[6]:
        m3=swap(m3)

    if c1!=message[4] and c2==message[5] and c3!=message[6]:
        m2=swap(m2)

    if c1!=message[4] and c2!=message[5] and c3!=message[6]:
        m4=swap(m4)

    final_message.append(m1)
    final_message.append(m2)
    final_message.append(m3)
    final_message.append(m4)
    return final_message




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
    liste_2 = []
    
    # Si la liste est en base 16...
    for i in range(len(liste)):
        if liste[i] == "A":
            liste_2.append(10)
        elif liste[i] == "B":
            liste_2.append(11)
        elif liste[i] == "C":
            liste_2.append(12)
        elif liste[i] == "D":
            liste_2.append(13)
        elif liste[i] == "E":
            liste_2.append(14)
        elif liste[i] == "F":
            liste_2.append(15)
        else:
            liste_2.append(int(liste[i]))
    
    for i in range(len(liste_2)):
        integer += liste_2[-i-1]*(base**i)
    
    return integer


def show_base_hexa(liste):
    """
    Fonction qui retourne un nombre en base 16.
    """
    message = []
    for v in liste:
        if(v == 10):
            message.append("A")
        elif(v == 11):
            message.append("B")
        elif(v == 12):
            message.append("C")
        elif(v == 13):
            message.append("D")
        elif(v == 14):
            message.append("E")
        elif(v == 15):
            message.append("F")
        else:
            message.append(str(v))
    return message
   

def translate_hexa(matrix):
    """
    Fonction qui traduit et retourne en hexadécimal les données de la matrice.
    """
    message = []
    for i in range(nbrLig(matrix)):
        matrix[i] = conversion_integer(matrix[i],2)

    matrix = show_base_hexa(matrix)
    
    for i in range(0,nbrLig(matrix),2):
        message.append(matrix[i]+ matrix[i+1])

    for i in range(nbrLig(message)):
        message[i] = conversion_integer(message[i],16)

    for i in range(nbrLig(message)):
        print(chr(message[i]))

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
