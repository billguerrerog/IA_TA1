from tkinter import * 
from tkinter import ttk 
from math import e
import random
import numpy as np

root = Tk()
root.geometry("600x250")
root.title("Simulated Annealing - Courier")

##Funciones
#Generar una ruta
def GenerarRuta(mapa):
    n = len(mapa)
    ruta = [None] * n
    cont = 0
    while True:
        if cont==n:
            break
        val = random.randint(0, n-1)
        if val in ruta:
            continue
        ruta[cont] = val
        cont += 1
    return ruta

#Cálculo del tiempo, de acuerdo con la distancia total
def CalcularTiempo(mapa,SolActual):
    horaXkm = 1/40 #40km/h - 0.025 horas por kilómetro
    ruta = []
    suma_distancia = 0
    for i in range(len(SolActual) - 1):
        ruta.append(mapa.item(SolActual[i], SolActual[i + 1]))
        suma_distancia = suma_distancia + ruta[i]
    tiempo_total = horaXkm * suma_distancia
    return tiempo_total

#Implementación de Algoritmo Simulated Annealing
def SimulatedAnnealing(mapa,rutaActual):
    solActual = rutaActual
    temp = 1000
    enfriamiento = 0.005
    while temp >= 0.0015:
        solNueva = GenerarRuta(mapa)
        tiempo_actual = 0
        tiempo_nuevo = 0
        for i in range(0,len(mapa)-1):
            distActual = mapa[solActual[i],solActual[i+1]]
            distNueva = mapa[solNueva[i],solNueva[i+1]]
            tiempo_actual += distActual
            tiempo_nuevo += distNueva

        #Se minimiza la distancia
        probabilidad_cambio = 0.0000000000
        if tiempo_nuevo < tiempo_actual:
            probabilidad_cambio = 1.0000000000
        else:
            probabilidad_cambio = (e)**((tiempo_actual-tiempo_nuevo)/(temp))

        #De acuerdo a la probabilidad se realiza el cambio o no
        coef = random.randint(0,100)
        if coef/100 <= probabilidad_cambio:
            solActual = [] + solNueva

        #Bajar temperatura
        temp = temp*(1-enfriamiento)

    return solActual  

#Generar mapa de acuerdo con el número de puntos de entrega
def GenerarMapa(num):
    n=int(num)
    mapa = []
    for i in range(n):
      fil = []
      for j in range(n):
        fil.append(None)
      mapa.append(fil)  

    for j in range(n):
      i = j
      while True:
        if i == n:
          break
        if i == j :
          mapa[i][j] = 0
        else:    
          dist = random.randint(5,50)
          mapa[i][j] = dist
          mapa[j][i] = dist
        i += 1
    return np.matrix(mapa)

def matriz(puntos_entrega):
    top = Toplevel()
    top.title("Matriz Generada")
    global mapa
    mapa=GenerarMapa(puntos_entrega)

    global rutaActual
    global rutaNueva
    rutaActual,rutaNueva = [],[]
    rutaActual = generar_ruta_inicial(mapa)
    my_label= Label(top, text=mapa).pack()

def MatrizPrueba(puntos_entrega):
    mapa=GenerarMapa(puntos_entrega)
    rutaActual,rutaNueva = [],[]
    rutaActual = generar_ruta_inicial(mapa)
    return mapa,rutaActual

def generar_ruta_inicial(mapa):
    rutaInicial =[]
    for i in range(len(mapa)):
        rutaInicial.append(i)
    return rutaInicial

def SolucionPrueba(mapa,ruta_act):
    solucionFinal = SimulatedAnnealing(mapa,ruta_act)
    return solucionFinal

# Vista Solución
def solucion():
    top = Toplevel()
    top.title("Solución")
    top.geometry("600x400")
    solucionFinal = SimulatedAnnealing(mapa,rutaActual)
    rutaIn=generar_ruta_inicial(mapa)
    tiempo_inicial = CalcularTiempo(mapa,rutaIn)
    costo_final = CalcularTiempo(mapa,solucionFinal)
    rutaIText=Label(top,text="Ruta Inicial: ",height=3,font=10)
    rutaI=Label(top,text=rutaIn,height=3,font=10)
    CIT=Label(top,text="Tiempo Inicial: ",height=3,font=10)
    CI=Label(top,text=tiempo_inicial,height=3,font=10)
    espacio2 = Label(top, text="               ")
    rutaOT=Label(top,text="Ruta Optimizada: ",height=3,font=10)
    rutaO=Label(top,text=solucionFinal,height=3,font=10)
    COT=Label(top,text="Tiempo Optimizado: ",height=3,font=10)
    CO=Label(top,text=costo_final,height=3,font=10)

    rutaIText.grid(row=0,column=0)
    rutaI.grid(row=0,column=1)
    CIT.grid(row=1,column=0)
    CI.grid(row=1,column=1)
    espacio2.grid(row=2, column=0)
    rutaOT.grid(row=3,column=0)
    rutaO.grid(row=3,column=1)
    COT.grid(row=4,column=0)
    CO.grid(row=4,column=1)
    return solucionFinal

#Vista Pruebas
def Pruebas():
    top = Toplevel()
    top.title("Pruebas")
    top.geometry("250x300")

    top1 = Toplevel()
    top1.title("Pruebas")
    top1.geometry("500x250")

    # Create A main frame
    main_frame= Frame(top1)
    main_frame.pack(fill=BOTH,expand=1)

    # Create A canvas 
    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT,fill=BOTH, expand=1)

    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL,command=canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)

    canvas.configure(yscrollcommand=scrollbar)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))
    
    second_frame = Frame(canvas)

    canvas.create_window((0,0),window=second_frame,anchor="nw")

    fallas = 0
    exito = 0
    iguales = 0
    n = 10
    for i in range(n):
        n=i+1
        mapa1,ruta_act=MatrizPrueba(5)
        solucionActual=SolucionPrueba(mapa1,ruta_act)
        if CalcularTiempo(mapa1,generar_ruta_inicial(mapa1)) > CalcularTiempo(mapa1,solucionActual):
            exito += 1
        elif CalcularTiempo(mapa1,generar_ruta_inicial(mapa1)) < CalcularTiempo(mapa1,solucionActual):
            fallas += 1
        else:
            iguales += 1
        Label(second_frame,text="Prueba ").grid(row=i,column=0)
        Label(second_frame,text=n).grid(row=i,column=1)
        Label(second_frame,text="Tiempo Inicial: ").grid(row=i,column=2)
        Label(second_frame,text=CalcularTiempo(mapa1,generar_ruta_inicial(mapa1))).grid(row=i,column=3)
        Label(second_frame,text="Tiempo Final: ").grid(row=i,column=4)
        Label(second_frame,text=CalcularTiempo(mapa1,solucionActual)).grid(row=i,column=5)

    #Widgets & Grid System
    PET=Label(top,text="Pruebas exitosas: ",height=3,font=10)
    PE=Label(top,text=exito,height=3,font=10)
    PFT=Label(top,text="Pruebas fallidas: ",height=3,font=10)
    PF=Label(top,text=fallas,height=3,font=10)
    PIT=Label(top,text="Sin cambio: ",height=3,font=10)
    PI=Label(top,text=iguales,height=3,font=10)
    PET.grid(row = 0, column = 0)
    PE.grid(row = 0,column = 1)
    PFT.grid(row = 1,column = 0)
    PF.grid(row = 1,column = 1)
    PIT.grid(row = 2,column = 0)
    PI.grid(row = 2,column = 1)

##Vista principal
#Widgets
puntos_entrega = Label(root, text="N° Puntos de Entrega",height=3,font=10)
espacio = Label(root, text="               ")
numero_puntos_entrega = Entry(root, width=30)
generar_matriz = Button(root, text="Generar Matriz", command=lambda: matriz(numero_puntos_entrega.get()))
Solucion = Button(root, text="Ver Solución",command=solucion)
label = Label(root, text="10 casos con 5 puntos de entrega",height=3,font=10)
pruebas = Button(root, text="Ver Pruebas",command=Pruebas)

#Grid System
puntos_entrega.grid(row=0,column=2)
numero_puntos_entrega.grid(row=0, column=3)
generar_matriz.grid(row=1, column=2)
Solucion.grid(row=1, column=3)
espacio.grid(row=2, column=0)
label.grid(row=3,column=2)
pruebas.grid(row=3, column=3)

root.mainloop()


