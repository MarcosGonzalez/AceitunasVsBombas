#! /usr/bin/env python

import pilas
import random
import ConfigParser
from pilas.escena import Base
from bomba import BombaConMovimiento
archivo = "puntajes.ini"

class Menu(Base):
    """Esta clase representa el menu principal del juego"""

    def __init__(self):
        """Esta es la funcion inicial del programa"""
        Base.__init__(self)

    def iniciar(self):
        """En esta funcion se definen variables de la clase y se crea el actor Menu"""
        self.fondo = pilas.fondos.Noche()
        self.crear_menu()
        
    def crear_menu(self):
        """Esta funcion crea un menu de opciones en base a cuatro funciones"""
        def iniciar_juego(): # inicia el juego
            pilas.cambiar_escena(Juego())
        def creditos(): # ejecuta los creditos
            pilas.cambiar_escena(Creditos())
        def ayuda_iniciar(): # ejecuta la ayuda
            pilas.cambiar_escena(Ayuda())
        def salir_del_juego(): # sale del juego
            pilas.terminar()

        self.menu = pilas.actores.Menu([("Iniciar Juego", iniciar_juego),
                                        ("Creditos", creditos),
                                        ("Ayuda", ayuda_iniciar),
                                        ("Salir", salir_del_juego),
                                        ])



class Juego(Base):
    """esta es la escena donde se desarrolla el juego"""

    def __init__(self, bombas=4, puntaje='0'):
        """Esta es la funcion inicial del programa"""
        Base.__init__(self)
               
        self.contador = bombas
        self.puntos = puntaje
        
    def iniciar(self):
        """crea las variables de la clase"""
        self.fondo = pilas.fondos.Espacio()
        self.bombas = []
        self.ganaste = pilas.sonidos.cargar("/home/usuario/Escritorio/AceitunasVsBombas/shrek_trumpets.mp3")
        self.perdiste = pilas.sonidos.cargar("/home/usuario/Escritorio/AceitunasVsBombas/perdedor.mp3")
        self.puntaje=pilas.actores.Puntaje(self.puntos, x=280, y=200)
        self.puntaje.color = pilas.colores.blanco
        self.musica = pilas.sonidos.cargar("/home/usuario/Escritorio/AceitunasVsBombas/hola.wav")
        self.musica.reproducir()
        self.moneda = pilas.actores.Moneda()
        x = random.randint(-320, 320)
        y = random.randint(-240, 240)
        self.moneda.x, self.moneda.y = x, y        
        for i in range(self.contador):
            x = random.randint(-320, 320)
            y = random.randint(-240, 240)
            
            self.bombas.append(BombaConMovimiento(x=x, y=y))
            for i in range(len(self.bombas)):
                self.bombas[i].escala = 0.65 
        def funcion_iniciar():
            """Esta es la clase que se ejecuta al ganar un nivel del juego"""
            self.aumentar.terminar()
            self.contador += 1
            for i in range(len(self.bombas)):
                self.bombas[i].eliminar()
            self.ganaste.reproducir()
            protagonista.reir()
            fondo = pilas.fondos.Fondo("/home/usuario/Escritorio/AceitunasVsBombas/bigstock_You_Win_Road_Sign_4335631.jpg")
            fondo.escala = 1.60 
            texto=pilas.actores.Texto("GANASTE!!")
            texto.y=70
            texto.color = pilas.colores.negro
            def siguiente_nivel(): # Avanza al siguiente nivel
                pilas.cambiar_escena(Juego(self.contador, self.puntaje.obtener_texto()))
                self.ganaste.detener()
            menu = pilas.actores.Menu([("Siguiente Nivel", siguiente_nivel)])
            texto2=pilas.actores.Texto("Tu puntaje: " + self.puntaje.obtener_texto())
            texto2.y=-70
            texto2.color = pilas.colores.negro 
            menu.color = pilas.colores.azul        
            self.musica.detener()
            self.moneda.eliminar()
        def aumentar(puntaje): # Es la funcion que se encarga de aumentar el puntaje 
            puntaje.aumentar(10)
            return True
        self.aumentar = pilas.mundo.agregar_tarea(2, aumentar, self.puntaje)
        self.temporizador = pilas.actores.Temporizador()
        self.temporizador.x = -280
        self.temporizador.y = 200
        self.temporizador.color = pilas.colores.blanco
        self.temporizador.ajustar(10, funcion_iniciar)
        self.temporizador.iniciar()
        protagonista = pilas.actores.Aceituna()
        protagonista.escala=0.65
        protagonista.aprender(pilas.habilidades.SeguirAlMouse)
        protagonista.aprender(pilas.habilidades.SeMantieneEnPantalla)
        pilas.mundo.motor.ocultar_puntero_del_mouse()
        protagonista.x, protagonista.y = 270, -220
        def cuando_colisionan3(protagonista, moneda):
            self.puntaje.definir_texto(str(int(self.puntaje.obtener_texto())+15))
            self.moneda.eliminar()
        def cuando_colisionan(protagonista, bombas):
            """Es la funcion que se ejecuta cuando se pierde"""
            protagonista.eliminar()
            for i in range(len(self.bombas)):
                self.bombas[i].eliminar()
            self.bombas = []
            for i in range(self.contador):
                x = random.randint(-320, 320)
                y = random.randint(-240, 240)
            
                self.bombas.append(BombaConMovimiento(x=x, y=y))
                for i in range(len(self.bombas)):
                    self.bombas[i].escala = 0.75
            
            protagonista2 = pilas.actores.Aceituna()
            protagonista2.escala=0.50
            protagonista2.aprender(pilas.habilidades.SeguirAlMouse)
            protagonista2.aprender(pilas.habilidades.SeMantieneEnPantalla)
            protagonista2.x, protagonista2.y = 270, -220
            pilas.mundo.motor.ocultar_puntero_del_mouse()
            av = pilas.avisar("ULTIMA VIDA!!")
            self.puntaje.definir_texto(str(int(self.puntaje.obtener_texto())-20))
            def cuando_colisionan4(protagonista2, moneda):
                self.puntaje.definir_texto(str(int(self.puntaje.obtener_texto())+15))
                self.moneda.eliminar()
            def cuando_colisionan2(protagonista2, bombas):
                """Es la funcion que se ejecuta cuando se pierde"""
                for i in range(len(self.bombas)):
                    self.bombas[i].eliminar()
                self.temporizador.eliminar()
                pilas.escena_actual().tareas.eliminar_todas()
                self.perdiste.reproducir()
                textoo=pilas.actores.Texto("PERDISTE!! =S")
                textoo.y=70
                textoo.color=pilas.colores.rojo
                texto3=pilas.actores.Texto("Tu puntaje: " + self.puntaje.obtener_texto())
                texto3.y=130
                texto3.color=pilas.colores.rojo
                fondo = pilas.fondos.Fondo("/home/usuario/Escritorio/AceitunasVsBombas/loser.png")
                fondo.escala = 1.30
                self.musica.detener()
                def iniciar_juego_de_nuevo(): #Inicia de nuevo el juego
                    pilas.cambiar_escena(Juego())
                def volver_menu(): #Vuelve al menu principal
                    pilas.mundo.motor.mostrar_puntero_del_mouse()
                    pilas.cambiar_escena(Menu())
                def salir_del_juego(): #sale del juego
                    pilas.terminar()
                self.moneda.eliminar()
                def guarda_puntaje():
                    pilas.mundo.motor.mostrar_puntero_del_mouse()
                    puntaje = self.puntaje.obtener_texto()
                    pilas.cambiar_escena(GuardarPuntaje(puntaje))
        
                menu = pilas.actores.Menu([("Reiniciar juego", iniciar_juego_de_nuevo),
                                           ("Volver al menu principal", volver_menu),
                                           ("Guardar puntaje", guarda_puntaje),
                                           ("Salir", salir_del_juego),
                                           ])
                menu.color = pilas.colores.rojo

            pilas.escena_actual().colisiones.agregar(protagonista2, self.bombas, cuando_colisionan2)
            pilas.escena_actual().colisiones.agregar(protagonista2, self.moneda, cuando_colisionan4)
        pilas.escena_actual().colisiones.agregar(protagonista, self.bombas, cuando_colisionan)
        pilas.escena_actual().colisiones.agregar(protagonista, self.moneda, cuando_colisionan3)
       
class GuardarPuntaje(Base):
    def __init__(self, puntaje):
        Base.__init__(self)
        self.puntaje = puntaje        
    def iniciar(self):        
        fondo = pilas.fondos.Tarde()
        titulo = pilas.actores.Texto("Ingresa tu  nombre." + "Tu puntaje es: " + str(self.puntaje))        
        ingreso = pilas.interfaz.IngresoDeTexto()  
        ingreso.y = -50
        boton = pilas.interfaz.Boton("Enviar")
        boton.y = -100
        def crear():
            try:
                ar = open(archivo, 'r')
                cosas = ar.read()
                ar.close
                arch = open(archivo, 'r+')
                arch.write(cosas + "\n" + str(ingreso.texto) + "," +str(self.puntaje))
                arch.close
                pilas.cambiar_escena(Menu())
            except:
                arch = open(archivo, 'r+')
                arch.write(str(ingreso.texto) + "," +str(self.puntaje))
                arch.close
                pilas.cambiar_escena(Menu())

            
        boton.conectar(crear)


        
        


class Creditos(Base):
    """Ejecuta los creditos del juego (Creadores y Agradecimientos)"""
    def __init__(self):
        Base.__init__(self)
        """Esta es la funcion inicial del programa"""
    def iniciar(self):
        """Crea las variables de la clase"""
        self.fondo = pilas.fondos.Noche()
        self.texto = pilas.actores.Texto("""
Creado por : Marcos Gonzalez 
==========

Agradecimientos : Nuestros agradecimientos al crack de Luciano Castillo y a Franco Agresta.
==============
    """)
        self.texto.x, self.texto.y = 0, 250
        self.texto.escala=0.70
        self.texto.y=[-30]
    
        def atras(): # Vuelve al munu principal   
            pilas.cambiar_escena(Menu())
        menu=pilas.actores.Menu([("Atras" , atras)])
        menu.x = -250
        menu.y = 200
    

class Ayuda(Base):
    """Ejecuta la Ayuda del juego (como se juega)"""
    def __init__(self):
        Base.__init__(self)
        """Esta es la funcion inicial del programa"""
    def iniciar(self):
        """Crea las variables de la clase"""
        self.fondo = pilas.fondos.Noche()
        self.texto = pilas.actores.Texto("""
Este juego es muy divertido y sencillo,
solo tienes que  mover  el  mouse  para
esquivar las bombas e intentar de durar
10 segundos para  ganar, pero  cuidado, 
que no te toquen  porque  si colisionas 
alguna perderas, suerte!!
        """)
        self.texto.x, self.texto.y = 30, 250
        self.crear_menu()

    def crear_menu(self):
        """crea otro menu para volver al principal"""
        def atras(): # Vuelve al menu principal
            pilas.cambiar_escena(Menu())
        self.menu2=pilas.actores.Menu([("Atras" , atras)])
        self.menu2.x = -250
        self.menu2.y = -200



pilas.iniciar(gravedad=(0,0), pantalla_completa=True)

pilas.cambiar_escena(Menu())

pilas.ejecutar()
