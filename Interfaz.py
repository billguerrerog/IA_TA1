from tkinter import * 
from tkinter import ttk 
from math import e
import random
import numpy as np


root = Tk()
root.geometry("600x300")

root.title("Simulated Anneling")
'''
    Funciones 
'''

def GenerarRuta(mapa):
  n = len(mapa)
  ruta = [None] * n
  cont = 0
  while True:   
    if cont==n:
      break
    val = random.randint(0,n-1)
    if val in ruta:
      continue 
    ruta[cont] = val
    cont += 1
  return ruta

def calcular_costo_gasolina(mapa,SolActual):
    costoxgalon = 16.17
    galones = 9.25 / 100
    ruta = []
    suma = 0
    for i in range(len(SolActual) - 1):
        ruta.append(mapa.item(SolActual[i], SolActual[i + 1]))
        suma = suma + ruta[i]
    costo_gasolina = galones * costoxgalon * suma
    return costo_gasolina


def simulatedAnneling(mapa,rutaActual):
    solActual = rutaActual
    temp = 1000
    Fenfri = 0.005
    while temp>=0.0015:
        solNueva = GenerarRuta(mapa)
        energiaActual = 0
        energiaNueva = 0 
        for i in range(0,len(mapa)-1):
            distActual = mapa[solActual[i],solActual[i+1]]
            distNueva = mapa[solNueva[i],solNueva[i+1]]
            energiaActual += distActual
            energiaNueva += distNueva
        #minimizar distancias
        probCambio = 0.0000000000
        if energiaNueva < energiaActual:
            probCambio = 1.0000000000
        else:
            probCambio = (e)**((energiaActual-energiaNueva)/(temp)) 
        ##DADO LA probabilidad podremos hacer el cambio
        coef = random.randint(0,100)
        if coef/100 <= probCambio:
            solActual = [] + solNueva
        #Bajar temperatura
        temp = temp*(1-Fenfri)

    return solActual  



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
          dist = random.randint(85,324)
          mapa[i][j] = dist
          mapa[j][i] = dist
        i += 1
    return np.matrix(mapa)

def matriz(Ciudad):
    top = Toplevel()
    top.title("Matriz Generado")
    global mapa
    mapa=GenerarMapa(Ciudad)

    global rutaActual
    global rutaNueva
    rutaActual,rutaNueva = [],[]
    rutaActual = generar_ruta_inicial(mapa)
    my_label= Label(top, text=mapa).pack()

def matriz1(Ciudad):
    mapa=GenerarMapa(Ciudad)
    rutaActual,rutaNueva = [],[]
    rutaActual = generar_ruta_inicial(mapa)
    return mapa,rutaActual

def generar_ruta_inicial(mapa):
    rutaInicial =[]
    for i in range(len(mapa)):
        rutaInicial.append(i)
    return rutaInicial

def solucion1(mapa,ruta_act):
    solucionFinal = simulatedAnneling(mapa,ruta_act)
    rutaIn=generar_ruta_inicial(mapa)
    costoInicial = calcular_costo_gasolina(mapa,rutaIn)
    costoFinal = calcular_costo_gasolina(mapa,solucionFinal)
    return solucionFinal

def solucion():
    top = Toplevel()
    top.title("Solución")
    top.geometry("600x300")
    solucionFinal = simulatedAnneling(mapa,rutaActual)
    rutaIn=generar_ruta_inicial(mapa)
    costoInicial = calcular_costo_gasolina(mapa,rutaIn)
    costoFinal = calcular_costo_gasolina(mapa,solucionFinal)
    rutaIText=Label(top,text="Ruta Inicial: ",height=5,font=10)
    rutaI=Label(top,text=rutaIn,height=5,font=10)
    CIT=Label(top,text="Costo Inicial: ",height=5,font=10)
    CI=Label(top,text=costoInicial,height=5,font=10)
    rutaOT=Label(top,text="Ruta Optimizada: ",height=5,font=10)
    rutaO=Label(top,text=solucionFinal,height=5,font=10)
    COT=Label(top,text="Costo Optimizado: ",height=5,font=10)
    CO=Label(top,text=costoFinal,height=5,font=10)

    rutaIText.grid(row=0,column=0)
    rutaI.grid(row=0,column=1)
    CIT.grid(row=1,column=0)
    CI.grid(row=1,column=1)
    rutaOT.grid(row=0,column=2)
    rutaO.grid(row=0,column=3)
    COT.grid(row=1,column=2)
    CO.grid(row=1,column=3)
    return solucionFinal


def Pruebas():
    top = Toplevel()
    top.title("Pruebas")
    top.geometry("200x700")

    
    top1 = Toplevel()
    top1.title("Pruebas")
    top1.geometry("600x600")


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
        mapa1,ruta_act=matriz1(5)
        solucionActual=solucion1(mapa1,ruta_act)
        if calcular_costo_gasolina(mapa1,generar_ruta_inicial(mapa1)) > calcular_costo_gasolina(mapa1,solucionActual):
            exito += 1
        elif calcular_costo_gasolina(mapa1,generar_ruta_inicial(mapa1)) < calcular_costo_gasolina(mapa1,solucionActual):
            fallas += 1
        else:
            iguales += 1
        Label(second_frame,text="Prueba ").grid(row=i,column=0)
        Label(second_frame,text=n).grid(row=i,column=1)
        Label(second_frame,text="Costo Inicial: ").grid(row=i,column=2)
        Label(second_frame,text=calcular_costo_gasolina(mapa1,generar_ruta_inicial(mapa1))).grid(row=i,column=3)
        Label(second_frame,text="Costo Final: ").grid(row=i,column=4)
        Label(second_frame,text=calcular_costo_gasolina(mapa1,solucionActual)).grid(row=i,column=5)
    PET=Label(top,text="Pruebas exitosas: ",height=5,font=10)
    PE=Label(top,text=exito,height=5,font=10)
    PFT=Label(top,text="Pruebas fallidas: ",height=5,font=10)
    PF=Label(top,text=fallas,height=5,font=10)
    PIT=Label(top,text="Iguales: ",height=5,font=10)
    PI=Label(top,text=iguales,height=5,font=10)
    PET.grid(row = 0, column = 0)
    PE.grid(row =1,column = 0)
    PFT.grid(row =2,column = 0)
    PF.grid(row =3,column = 0)
    PIT.grid(row =4,column = 0)
    PI.grid(row =5,column = 0)


'''
    Creacion de widgets
'''
Ciudades = Label(root, text="N° Ciudades",height=5,font=10)
espacio = Label(root, text="               ")
numero_ciudad = Entry(root, width=40)
Grafo_generado = Button(root, text="Ver matriz generado", command=lambda: matriz(numero_ciudad.get()))
Solucion = Button(root, text="Ver Solucion",command=solucion)
label = Label(root, text="5 Ciudades y 10 Casos de uso",height=5,font=10)
pruebas = Button(root, text="Ver Pruebas",command=Pruebas)



'''
    Sistema grid
'''
Ciudades.grid(row=0,column=2)
numero_ciudad.grid(row=0, column=3)
Grafo_generado.grid(row=1, column=2)
Solucion.grid(row=1, column=3)
espacio.grid(row=2, column=0)
label.grid(row=3,column=2)
pruebas.grid(row=4, column=2)


root.mainloop()


