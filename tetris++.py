import tetris
import gamelib
ESPERA_DESCENDER = 8
def juego_crear():
    pieza = tetris.generar_pieza(None)
    juego = tetris.crear_juego(pieza)
    return juego

def juego_actualizar(juego, tecla, dic, rotaciones):
    """
    agregue las teclas como claves de un dic y lo valores como movimientos
    """
    dic[tecla] = dic.get(tecla,[None])
    if dic[tecla] == None:
        return juego
    if dic[tecla] ==  "IZQUIERDA":
        juego = tetris.mover(juego,tetris.IZQUIERDA)         
    if dic[tecla] == "DERECHA":
        juego = tetris.mover(juego,tetris.DERECHA)
    if dic[tecla] == "DESCENDER":
        siguiente_pieza = tetris.generar_pieza(None)
        juego, _ = tetris.avanzar(juego, siguiente_pieza) 
    if dic[tecla] == "ROTAR":
        juego = tetris.rotar(juego, rotaciones)  
    if dic[tecla] == "GUARDAR":
        ruta = "partida_tetris.txt"
        tetris.guardar_partida(juego,ruta)
    if dic[tecla] == "CARGAR":
        ruta = "partida_tetris.txt"
        pieza, grilla = tetris.cargar_partida(ruta)
        juego = pieza, grilla
    if dic[tecla] == "SALIR":
        condicion_de_salida = False
    
            
    return juego

    
def lineas_laterales_tetris():
    gamelib.draw_line(150, 0, 150, 500, fill='blue', width=2)
    gamelib.draw_line(350, 0, 350, 500, fill='blue', width=2)
    gamelib.draw_rectangle(0, 0, 150,400, outline="blue", fill='black')
    gamelib.draw_rectangle(350, 0, 500,400, outline="blue", fill='black')
    gamelib.draw_image('img/letras.gif', 18,40)
    gamelib.draw_image('img/score.gif', 15 ,150)
    gamelib.draw_line(15, 30, 135, 30, fill='blue', width=1) 
    gamelib.draw_line(15, 110, 135, 110, fill='blue', width=1)
    gamelib.draw_line(15, 30, 15, 110, fill='blue', width=1)
    gamelib.draw_line(135, 30, 135, 110, fill='blue', width=1)
    
def juego_mostrar(juego):
    pieza_actual = tetris.pieza_actual(juego)
    grilla = tetris.eliminar_linea_del_juego(juego)
    gamelib.draw_image('img/estrella.gif', -300,-100 ) 
    lineas_laterales_tetris()
    for x in range(tetris.ANCHO_JUEGO):
        for y in range(tetris.ALTO_JUEGO):
            if tetris.hay_superficie(juego, x, y): 
                pos_y = y*22.2
                pos_x = 22.2*x - 88.8
                gamelib.draw_rectangle(238.8 + pos_x, 0 + pos_y ,261.38 + pos_x , 22.22 + pos_y, outline='black', fill="yellow")     
    for x,y in pieza_actual:
        pos_y = y*22.2
        pos_x = 22.2*x - 88.8
        gamelib.draw_rectangle(238.8 + pos_x, 0 + pos_y ,261.38 + pos_x , 22.22 + pos_y, outline='black', fill="yellow")
def puntuaciones():
    with open("puntuaciones.txt") as f:
        lista_puntaje = [] 
        lista_de_puntajes = []
        for linea in f:
            lista_puntaje = linea.split(",")
            if linea == "\n":
                continue
            nombre, puntaje = lista_puntaje
            tupla = int(puntaje), nombre
            lista_de_puntajes.append(tupla)
    lista_de_puntajes.sort() 
    lista_de_puntajes.reverse()
    while len(lista_de_puntajes) >= 11: 
        lista_de_puntajes.pop()
    return lista_de_puntajes
   
          
def mostrar_puntuaciones(lista_de_puntajes):
    y = 0
    ranking = 0
    gamelib.draw_text(f'HIGHSCORES',375 , 40 , fill='blue', anchor='nw')
    for x in range(len(lista_de_puntajes)):
            nombre = lista_de_puntajes[x][1]
            puntaje = lista_de_puntajes[x][0]
            ranking = ranking + 1 
            y = y + 20
            gamelib.draw_text(f'{ranking}. {nombre} : {puntaje}',375 , 50 + y, fill='white', anchor='nw')

def leer_archivo_teclas():
    dic_teclas = {}
    with open("teclas.txt") as f:
        for linea in f:
            campos = linea.rstrip().split("=")
            letra, movimiento = campos
            dic_teclas[letra.rstrip()] = movimiento.lstrip()  
    return dic_teclas                    
def main():
    juego = juego_crear()
    # Inicializar el estado del juego
    gamelib.resize(500, 400)
    condicion_de_salida = True
    score = 0
    timer_bajar = ESPERA_DESCENDER
    dic_teclas = leer_archivo_teclas()
    rotaciones = tetris.buscar_rotaciones()
    puntajes = puntuaciones()
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        juego_mostrar(juego)
        if tetris.terminado(juego):
            mostrar_puntuaciones(puntajes) 
        gamelib.draw_text(score, 70, 200) 
        gamelib.draw_end()
        if condicion_de_salida == False:
            break
        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress:
              tecla = event.key
              juego = juego_actualizar(juego, tecla, dic_teclas, rotaciones)
              """
              para cerrar el juego con escape o cuando queres guardar el juego
              """
              if tecla == "Escape":
                  condicion_de_salida = False
              if tecla == "g":
                  condicion_de_salida = False 
              
                         
              
              # Actualizar el juego, según la tecla presionada

        timer_bajar -= 1  
        if timer_bajar == 0:
            if not tetris.terminado(juego):
                score = score + 50
            else:
                nombre = gamelib.input("Ingrese su nombre: ") 
                if len(puntajes) < 10:
                    with open("puntuaciones.txt","a") as f:
                        f.write(f"{nombre},{score}\n")
                if len(puntajes) >= 10 and puntajes[9][0] < score:
                    with open("puntuaciones.txt","w") as f:
                        tupla = score, nombre
                        puntajes.append(tupla)
                        for x in range(len(puntajes)):
                            nombre = puntajes[x][1]
                            puntaje = puntajes[x][0]
                            f.write(f"{nombre},{puntaje}\n")
                break    
            timer_bajar = ESPERA_DESCENDER
            siguiente_pieza = tetris.generar_pieza(None)
            juego, _ = tetris.avanzar(juego, siguiente_pieza) 
            # Descender la pieza automáticamente

gamelib.init(main)