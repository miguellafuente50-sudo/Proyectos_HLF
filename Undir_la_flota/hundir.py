import random
#Funció crear barcos fijos
# tipos_barco = {
# 1:4,
# 2:3,
# 3:2,
# 4:3
# }
tipos_barco = {
1:1
}

#Creamos la función tblero
def crear_tablero(x=10, y=10):
    tablero = []
    for i in range(y):
        fila = []
        for j in range(x):
            fila.append("~")
        tablero.append(fila)

    return tablero

def conseguir_celda_libre(tablero, longitud, direccion):
    fila_maxima = len(tablero)-1
    columna_maxima = len(tablero[0])-1
    if direccion == "Horizontal":
        columna_maxima = len(tablero[0]) - longitud
    if direccion == "Vertical":
        fila_maxima = len(tablero) - longitud

    while True:
        fila = random.randint(0, fila_maxima)
        columna =  random.randint(0,columna_maxima)
        fila_actual = fila
        columna_actual = columna
        ocupado = False
        for i in range(0, longitud):
            if tablero[fila_actual][columna_actual] == "B":
                ocupado = True
                break
            if direccion == "Horizontal":
                columna_actual += 1
            elif direccion == "Vertical":
                fila_actual += 1
        if not ocupado:
            return fila, columna


def crear_barco(tablero, longitud, direccion="Horizontal"):
    fila, columna = conseguir_celda_libre(tablero, longitud, direccion)
    fila_actual = fila
    columna_actual = columna
    for i in range(0, longitud):
        tablero[fila_actual][columna_actual] = "B"
        if direccion == "Horizontal":
            columna_actual += 1
        elif direccion == "Vertical":
            fila_actual += 1


def crear_direccion():
    if random.random() < 0.5:
        return "Vertical"
    else:
        return "Horizontal"



def crear_barcos(tablero,tipos_barco):
    for tipo in tipos_barco:
        longitud = tipo
        for i in range(tipos_barco[tipo]):
            direccion = crear_direccion()
            crear_barco(tablero, longitud, direccion)


def disparar(tablero, fila, columna):
    if tablero[fila][columna] == "B":
        tablero[fila][columna] = "~"
        print("¡Has dado!")
        return True
    else:
        print("Agua")
        return False

def quedan_barcos(tablero):
    for fila in range(len(tablero)):
        for columna in range(len(tablero[fila])):
            if tablero[fila][columna] == "B":
                return True
    return False 

def introducir_fila_columna(tablero):
    fila_maxima = len(tablero)-1
    columna_maxima = len(tablero[0])-1
    while True :
        fila = int(input(f"Introduce un numero que sera el eje x de 0 a {fila_maxima} : "))
        if  fila < 0 or fila > fila_maxima:
            print("La fila  no esta dentro del tablero")
            continue
        columna = int(input(f"Introduce un numero que sera el eje y de 0 a {columna_maxima}: "))
        if columna < 0 or columna > columna_maxima:
            print("La columna no esta dentro del tablero")
            continue
        return fila, columna 


def fila_columna_aleatoria(tablero):
    fila_maxima = len(tablero)-1
    columna_maxima = len(tablero[0])-1
    fila = random.randint(0, fila_maxima)
    columna =  random.randint(0,columna_maxima)
    return fila, columna

def mostrar_tablero(tablero):
    columnas =[]
    for columna in range(len(tablero[0])):
        columnas.append(str(columna))
    print(" ",columnas)
    for fila in range(len(tablero)):
        print(fila, tablero[fila])





def jugar():
    tablero1 = crear_tablero()#Tablero juagdor 
    crear_barcos(tablero1, tipos_barco)
    tablero2 = crear_tablero()#Tablero IA
    crear_barcos(tablero2, tipos_barco)
    turno = 1
    while True:
        mostrar_tablero(tablero2)
        if turno == 1:#Jugador 
            print("Turno del jugador")
            fila, columna = introducir_fila_columna(tablero2)
            acierto = disparar(tablero2, fila, columna)
            if not acierto:
                turno = 2
            else:
                if not quedan_barcos(tablero2):
                    print("¡Has ganado!")
                    return 1
        if turno == 2:#IA
            print("Turno de la IA")
            fila, columna = fila_columna_aleatoria(tablero1)
            acierto = disparar(tablero1, fila, columna)
            if not acierto:
                turno = 1
            else:
                if not quedan_barcos(tablero1):
                    print("¡Puto pringado!")
                    return 2

jugar()