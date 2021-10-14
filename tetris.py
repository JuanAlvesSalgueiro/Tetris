ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)

import random
def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if pieza == None:
        pieza = random.randint(0,6) 
    return PIEZAS[pieza]   

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada = []
    for x,y in pieza:
        nueva_x = x + dx
        nueva_y = y + dy
        pieza_trasladada.append((nueva_x,nueva_y))
    return tuple(pieza_trasladada)                            

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    pieza_actual = trasladar_pieza(pieza_inicial,ANCHO_JUEGO//2,0)
    grilla = []
    for fila in range(ALTO_JUEGO):
        fila = []
        for c in range(ANCHO_JUEGO):
            fila.append(None)
        grilla.append(fila)  
    juego =  pieza_actual,grilla
    return juego 
def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    dimensiones = (ANCHO_JUEGO,ALTO_JUEGO)
    return dimensiones

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    pieza_actual = juego[0]
    return pieza_actual

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    grilla = juego[1]
    if grilla[y][x] == None:
        return False
    if grilla[y][x] == True:
        return True

def buscar_rotaciones():
    pieza = []
    rotaciones_de_una_pieza = []
    lista_de_rotaciones = []
    with open("piezas_v2.txt") as rotaciones:
        for rotaciones in rotaciones:
            rotaciones = rotaciones.split(" ")
            if rotaciones_de_una_pieza != []: 
                lista_de_rotaciones.append(rotaciones_de_una_pieza)
                rotaciones_de_una_pieza = []
            for tuplas in rotaciones:
                tuplas = tuplas.split(";")
                for numeros in tuplas:
                    numeros = numeros.split(",")
                    x,y = numeros
                    tupla = int(x),int(y)
                    pieza.append(tupla)
                    if len(pieza) == 4:
                        rotaciones_de_una_pieza.append(pieza)
                        pieza = []  
    lista_de_rotaciones.append(rotaciones_de_una_pieza)                   
    return lista_de_rotaciones 
def pieza_se_fue_de_la_grilla(pieza):
    for fila in range(len(pieza)):
        if pieza[fila][0] > 8 or pieza[fila][0] < 0:
            return True
    for x,y in pieza:
        if y == ALTO_JUEGO:
            return True
    else:
        return False

def rotar(juego, rotaciones):
    grilla = juego[1]                                
    pieza_actual = juego[0]
    pieza_rotar = sorted(pieza_actual)
    pos_1 = pieza_rotar[0]
    pieza_rotar = trasladar_pieza(pieza_rotar, - pos_1[0], - pos_1[1])
    pieza_rotar = list(pieza_rotar)
    for x in range(len(rotaciones)):
        if pieza_rotar in rotaciones[x]:
            indice_rotacion = rotaciones[x].index(pieza_rotar)
            if x == 0:
                pieza_rotar = rotaciones[x][indice_rotacion] 
            if 1 <= x <= 3:
                if indice_rotacion + 1 == 2:
                    pieza_rotar = rotaciones[x][0] 
                else:    
                    pieza_rotar = rotaciones[x][indice_rotacion + 1] 
            if x >= 4 :
                if indice_rotacion + 1 == 4:
                    pieza_rotar = rotaciones[x][0]
                else:
                    pieza_rotar = rotaciones[x][indice_rotacion + 1]
            pieza_rotar = trasladar_pieza(pieza_rotar,pos_1[0], pos_1[1] )
            if pieza_se_fue_de_la_grilla(pieza_rotar):
                return juego
            for x,y in pieza_rotar:
                if grilla[y][x] == True:
                    return juego    
            return pieza_rotar, grilla      
                             
   
def guardar_partida(juego, ruta):
    pieza_str = ""
    grilla_str = ""
    lista = []
    pieza_actual = juego[0]
    grilla = juego[1]
    for x,y in pieza_actual:
        pieza_str = pieza_str + str(x) + "," + str(y) + "-"
    for x in grilla:
        for elemento in x:
            lista.append(str(elemento))
    grilla_str = ",".join(lista)    
    with open(ruta, "w") as f:
        f.write(f"{pieza_str[:-1]}\n{grilla_str}")                     
def cargar_partida(ruta):
    pieza = []
    fila_de_la_grilla = []
    grilla = []
    with open(ruta) as f:
        for linea in f:
            linea = linea.rstrip().split("-")
            for tuplas in linea:
                numero = tuplas.split(",")
                x, y = numero
                tupla = int(x),int(y)
                pieza.append(tupla)
            break    
        for linea in f:
            linea = linea.rstrip().split(",")
            for x in linea: 
                if x == "None":
                    fila_de_la_grilla.append(None)    
                if x == "True":
                    fila_de_la_grilla.append(True)
                if len(fila_de_la_grilla) == 9:
                    grilla.append(fila_de_la_grilla)
                    fila_de_la_grilla = []                        
    return pieza, grilla       
          
             
def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    if terminado(juego):
        return juego
    pieza_mover = pieza_actual(juego)
    pieza_mover = trasladar_pieza(pieza_mover,direccion,0)
    grilla = juego[1]      
    if pieza_se_fue_de_la_grilla(pieza_mover):
        nuevo_juego = juego
        return nuevo_juego  
    for x,y in pieza_mover:
        if grilla[y][x] == True:
            nuevo_juego = juego
            return nuevo_juego
        else:
            nuevo_juego = pieza_mover,grilla                
    return nuevo_juego

def eliminar_linea_del_juego(juego):
    fila_vacia = []
    for columna in range(ANCHO_JUEGO):
        fila_vacia.append(None)
    grilla = juego[1]
    contador = 0
    for fila in range(len(grilla)):
        contador = 0
        for columna in range(len(grilla[0])):
            if grilla[fila][columna] == True:
                contador = contador + 1
            if contador == 9:
                grilla.remove(grilla[fila])
                grilla.insert(0,fila_vacia)
                contador = 0                   
    return grilla  


def avanzar(juego,siguiente_pieza):          
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """ 
    grilla = juego[1]
    if terminado(juego):
        cambiar_pieza = False
        return juego, cambiar_pieza 
    pieza_bajar = pieza_actual(juego)       
    pieza_bajar = trasladar_pieza(pieza_bajar,0,1)
    if pieza_se_fue_de_la_grilla(pieza_bajar):
        for x,y in juego[0]:
            grilla[y][x] = True
            cambiar_pieza = True
            grilla = eliminar_linea_del_juego(juego)
        siguiente_pieza = trasladar_pieza(siguiente_pieza,ANCHO_JUEGO//2,0)    
        juego_nuevo = siguiente_pieza,grilla 
        return juego_nuevo,cambiar_pieza 
    for x,y in pieza_bajar:
        if grilla[y][x] == True:
            for x,y in juego[0]:
                grilla[y][x] = True
                cambiar_pieza = True
                grilla = eliminar_linea_del_juego(juego)                
            siguiente_pieza = trasladar_pieza(siguiente_pieza,ANCHO_JUEGO//2,0)    
            juego_nuevo = siguiente_pieza,grilla 
            return juego_nuevo,cambiar_pieza                 
    juego_nuevo = pieza_bajar, grilla
    cambiar_pieza = False
    return juego_nuevo,cambiar_pieza     
           
def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    grilla = juego[1]
    for n in range(0,7):
        pieza_inicial = generar_pieza(n)
        pieza_inicial = trasladar_pieza(pieza_inicial,ANCHO_JUEGO//2,0)
        for x,y in pieza_inicial:
            if grilla[y][x] == True:
                return True   
    return False              
   
