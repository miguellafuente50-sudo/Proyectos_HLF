import random
import time


class Celda:# Representa una posición concreta de una parte del barco dentro del tablero.
            # Cada celda tiene una fila y una columna.
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        
    def esta_en(self, fila, columna):
        if fila == self.fila and columna == self.columna:
            return True
        else:
            return False
class Disparo:#ES una estructura similar a la celda, pero representa una posicion que ha habido un disparo.
    def __init__(self, fila, columna, acierto=False):
        self.fila = fila
        self.columna = columna
        self.acierto = acierto#Para poder diferenciar entre un disparo fallido y uno acertado.

    def esta_en(self, fila, columna):
            if fila == self.fila and columna == self.columna:
                return True
            else:
                return False



    #Representa un barco, su longitud, su dirección y las celdas que ocupa dentro del tablero.
class Barco:
    def __init__(self, fila, columna, longitud, direccion="Horizontal"):
        self.fila = fila
        self.columna = columna
        self.longitud = longitud
        self.direccion = direccion
        self.celdas = []
        self.construir()

    def construir(self):#Recorre la longirud del barco y crea una celda para cada posicion.
        fila_actual = self.fila
        columna_actual = self.columna
        for i in range(0, self.longitud):
            celda = Celda(fila_actual, columna_actual)
            self.celdas.append(celda)
            if self.direccion == "Horizontal":#si es horizontal sumamos uno a la columna que significa moverse uno a la derecha.
                columna_actual += 1
            elif self.direccion == "Vertical":#Abajo
                fila_actual += 1

    def esta_en(self, fila, columna):#Para cada celda del barco miramos si esta en la fila y columna qeu pasamos.
        for celda in self.celdas:
            if celda.esta_en(fila, columna):
                return True # si encotranos una sola celda del barco en la posicion significa que el barco esta ahi.
        return False #Si niguna celda estaba en esa posicion significa qeu el barco no esta.
    
    def esta_hundido(self):#Si la lita de celdas esta vacia el barco esta hundido. 
        if len(self.celdas) == 0:
            return True
        else:
            return False
        
    def recibir_danio(self, fila, columna):#Buscamos una celda que coicida en esa posicion y la quitamos de la lista.
        for celda in self.celdas:
            if celda.esta_en(fila, columna):
                self.celdas.remove(celda)



class Tablero:#Tablero representa el tablero de cada jugador.
    def __init__(self,filas=10,columnas=10):
        self.filas = filas
        self.columnas = columnas
        self.tipos_barco = { # La clave es la longitud de celdas de cada barco y el valor la cantidad de barcos.
                            1:4,
                            2:3,
                            3:2,
                            4:1
                            }
        self.barcos = [] 
        self.disparos = []
        self.crear_barcos() # inicializamos los barcos.
        
    def conseguir_celda_libre(self, longitud, direccion):#Busca una celda libre, teniendo en cuenta la longitud del barco para no salirse del tablero ni chocar con otros.
        fila_maxima = self.filas -1
        columna_maxima = self.columnas -1
        if direccion == "Horizontal":
            columna_maxima = self.columnas - longitud
        if direccion == "Vertical":
            fila_maxima = self.filas - longitud

        while True:#Si encuentra una celda ocupada vuelve a comenzar, sino recorre la lon del barco para saber si estan todas libres.
                fila = random.randint(0, fila_maxima)
                columna =  random.randint(0,columna_maxima)
                fila_actual = fila
                columna_actual = columna
                ocupado = False
                for i in range(0, longitud):
                    if self.barco_en(fila_actual, columna_actual):
                        ocupado = True
                        break
                    if direccion == "Horizontal":
                        columna_actual += 1
                    elif direccion == "Vertical":
                        fila_actual += 1
                if not ocupado:
                    return fila, columna # Devolvemos la posicion inicial del barco.

        
    def crear_direccion(self):#Genera una direccion de barco aleatoria.
        if random.random() < 0.5:
            return "Vertical"
        else:
            return "Horizontal"


    def crear_barco(self, longitud, direccion):
        fila, columna = self.conseguir_celda_libre(longitud, direccion)
        barco = Barco(fila, columna, longitud, direccion)
        self.barcos.append(barco)

    def crear_barcos(self):# Para cada tipo (longitud) creamos tantos barcos como nos dice el diccionario.
        for tipo in self.tipos_barco:
            longitud = tipo
            for i in range(self.tipos_barco[tipo]):
                direccion = self.crear_direccion()
                self.crear_barco(longitud, direccion)


    def barco_en(self, fila, columna):# Si alguno de los barcos del tablero esta en la possicion devuelve el barco.
        for barco in self.barcos:
            if barco.esta_en(fila, columna):
                return barco
        return None

    def disparo_en(self, fila, columna):# Si alguno de los disparos del tablero esta en esa posicion devolvemos disparo, para mostrarlos en el tablero.
            for disparo in self.disparos:
                if disparo.esta_en(fila, columna):
                    return disparo
            return None
    
                
    def disparar(self, fila, columna):#Buscamos un barco en esa fila y esa columna.
        barco = self.barco_en(fila, columna)
        if barco == None:#Si no hay barco añadimos un disparo fallido a la lista.
            disparo = Disparo(fila, columna)
            self.disparos.append(disparo)
            return False
        else:# Si hay barco recibe daño y añadimos un disparo acertado.
            barco.recibir_danio(fila, columna)
            disparo = Disparo(fila, columna, acierto=True)
            self.disparos.append(disparo)
            if barco.esta_hundido():#Si el barco esta hundido lo quitamos. 
                self.barcos.remove(barco)
                print("Barco Hundido")
            return True

    def mostrar(self, oculto=True):#Mostramos el tablero.
                columnas =[]
                for columna in range(self.columnas):#Mostramos un numero para cada columna.
                    columnas.append(str(columna))
                print("   "+" ".join(columnas))

                for i in range(self.filas):# Mostramos el tablero por filas.
                    fila = []
                    for j in range(self.columnas):
                        if self.barco_en(i, j) and not oculto :# Si hay un  barco en esa pocision y el tablero no esat oculto, mostramos el barco. 
                            fila.append("🚤")
                        elif self.disparo_en(i, j):# Si hay un  disparo en esa pocision mostramos el disparo en fincion si es acertado o fallido. 
                            disparo = self.disparo_en(i, j)
                            if disparo.acierto:
                                fila.append("💥")
                            else:
                                fila.append("💧")
                        else:# Si no mostramos agua
                            fila.append("🟦")
                    print(i, "".join(fila))# Mostramos el numero de filas y la fila.

    def contar_barcos(self):# Cuenta la cantidad de barcos que le quedan al tablero
        return len(self.barcos)  
    
    def ha_perdido(self):# Cuando noo quedan barco en el tablero devuelve false.
        if len(self.barcos) == 0 :
            return True
        else:
            return False




def introducir_fila_columna(tablero):# Lo hacemos en bucle por si el usuario se equivoca volver a preguntar.
    fila_maxima = tablero.filas - 1
    columna_maxima = tablero.columnas - 1
    while True :
        fila = int(input(f"Introduce la fila de 0 a {fila_maxima} : "))
        if  fila < 0 or fila > fila_maxima:
            print("La fila  no esta dentro del tablero")
            continue
        columna = int(input(f"Introduce la columna de  0 a {columna_maxima}: "))
        if columna < 0 or columna > columna_maxima:
            print("La columna no esta dentro del tablero")
            continue
        return fila, columna 


def fila_columna_aleatoria(tablero):# La IA lo usa para escoger su fila y columna.
    fila_maxima = tablero.filas -1
    columna_maxima = tablero.columnas -1
    fila = random.randint(0, fila_maxima)
    columna =  random.randint(0,columna_maxima)
    return fila, columna



def jugar():
    tablero1 = Tablero()#Tablero jugador 
    tablero2 = Tablero()#Tablero IA
    turno = 1
    while True:
        # Para cada jugada muestra el tablero y barcos enemigos, los del jugador y espera un segundo.
        print("=====================")
        print("Enemigo")
        print("_____________________")
        tablero2.mostrar()
        print("_____________________")
        print("Barcos:",tablero2.contar_barcos())
        print("=====================")
        print("Jugador")
        print("_____________________")
        tablero1.mostrar(oculto=False)
        print("_____________________")
        print("Barcos:",tablero1.contar_barcos())
        print("=====================")
        time.sleep(1)

        if turno == 1:#Jugador 
            print("Turno del jugador")
            fila, columna = introducir_fila_columna(tablero2)
            acierto = tablero2.disparar(fila, columna)
            if not acierto:
                print("¡Has fallado!")
                turno = 2
                continue
            else:
                print("¡Has acertado!")
                if tablero2.ha_perdido():
                    print("¡Has ganado!")
                    return 1
        if turno == 2:#IA
            print("Turno de la IA")
            time.sleep(1)
            fila, columna = fila_columna_aleatoria(tablero1)
            acierto = tablero1.disparar(fila, columna)
            if not acierto:
                print("¡La IA ha fallado!")
                turno = 1
            else:
                print("¡La IA ha acertado!")
                if tablero1.ha_perdido():
                    print("¡Puto pringado!")
                    return 2



jugar()

