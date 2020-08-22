from turtle import *
from random import seed
from random import randint
import turtle
import math


#Funcion ////////////////////////////////////////////////////////
def puntos():
    inicio=[randint(-300, 300),randint(-300, 300)];
    final=[randint(-300, 300),randint(-300, 300)];
    return [inicio,final]

def nuevo():
    x=randint(-300, 300);
    y=randint(-300, 300);
    return[x,y]

def prueba (punto,area):
    x_obstaculos=[]
    y_obstaculos=[]
    for i in range(len(area)):
        j=area[i]
        if punto[0]>=j[0] and punto[0]<=(j[0]+j[2]) and punto[1]>=j[1] and punto[1]<=(j[1]+j[3]):
            return 0
    return 1

def dibuja_obstaculo(matriz):
    for i in range(len(matriz)):
        objeto=matriz[i]
        flecha.begin_fill()
        flecha.goto(objeto[0],objeto[1])
        flecha.pendown()
        flecha.goto(objeto[0]+objeto[2],objeto[1])
        flecha.goto(objeto[0]+objeto[2],objeto[1]+objeto[3])
        flecha.goto(objeto[0],objeto[1]+objeto[3])
        flecha.goto(objeto[0],objeto[1])
        flecha.end_fill()
        flecha.penup()

def secciones(antes, nuevo,area):
    x_actual=antes[0]
    y_actual=antes[1]
    esc_x=(nuevo[0]-antes[0])/91
    esc_y=(nuevo[1]-antes[1])/91
    for i in range (90):
        for j in range (len(area)):
            obsta=area[j]
            if x_actual>=obsta[0] and x_actual<=(obsta[0]+obsta[2]) and y_actual>=obsta[1] and y_actual<=(obsta[1]+obsta[3]):
                return 0
        x_actual=x_actual+esc_x
        y_actual=y_actual+esc_y
    return 1

def calculo_Costo(costo,puntos,nodo,distancia,posicion):
    D_base=min(distancia)+radio_a;
    C_base=costo[posicion]
    for i in range(len(puntos)):
        test=distancia[i]
        C_new= costo[i]
        if test<=D_base and C_new<=C_base:
            cordenada=i 
    return cordenada

def dibujo(ruta):
    flecha.penup()
    s=ruta[0]
    flecha.goto(s[0],s[1])
    flecha.color("blue")
    flecha.pendown()
    for i in range(len(ruta)-1):
        segundo=ruta[i+1]
        flecha.goto(segundo[0],segundo[1]);
    

def dibujo2(ruta):
    flecha.penup()
    s=ruta[0]
    flecha.goto(s[0],s[1])
    flecha.color("red")
    flecha.pendown()
    for i in range(len(ruta)-1):
        segundo=ruta[i+1]
        flecha.goto(segundo[0],segundo[1]);


#entrada /////////////////////////////5//////////////////////////////////////
print("1=mapa con una linea en el centro")
print("2=mapa con un C donde se encierra el inicio")
print("3=mapa con un C donde se encierra el final")
print("4=mapa con un cruz")
print("5=contine el mapa 2 y 3")
print("en el caso de colocar algo diferente no existiran obstaculos")
tipo_mapa=input("Selecione el tipo de mapa:")

# ventana /////////////////////////////////////////////////////////////////////////
setup(700,700, 0, 0)
screensize(600, 600)
title("Algoritmo RRT*")

window = turtle.Screen()
flecha = turtle.Turtle()
flecha.hideturtle()
flecha.penup()
flecha.goto(-300,310)
flecha.pensize(2)
flecha.pendown()
flecha.forward(100)
flecha.penup()
flecha.goto(-300,-300)
flecha.speed(60)
flecha.pendown()
flecha.pensize(3)
for i in range(4):
    flecha.forward(600)
    flecha.left(90)

inicio=[150,150];
final=[-150,-200];

campo=[]
#[inicio,final]=puntos()
flecha.penup()
if tipo_mapa=="1":
    campo=[[-100,0,300,50]]
elif tipo_mapa=="2":
    campo=[[100,70,100,50],[100,80,40,100],[100,180,100,50]]
elif tipo_mapa=="3":
    campo=[[-200,-270,100,40],[-140,-230,40,100],[-200,-130,100,50]]
elif tipo_mapa=="4":
    campo=[[-100,0,300,50],[25,-125,50,300]]
elif tipo_mapa=="5":
    campo=[[100,70,100,50],[100,80,40,100],[100,180,100,50],[-200,-270,100,40],[-140,-230,40,100],[-200,-130,100,50]]
else:
    campo=[]
##Obstaculos visibles
dibuja_obstaculo(campo)


flecha.goto(final[0],final[1]);flecha.dot((15),"green")
flecha.goto(inicio[0],inicio[1]);flecha.dot((15),"gray")
flecha.color("orange")
#flecha.showturtle()

#Comandos ///////////////////////////////////////////////////////////////////
radio_a=100
radio_b=50
#Busqueda &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def rrt(campo,radio_a,radio_b,c_inicio,c_final):
    optenidos=[c_inicio]
    costo=[0]
    while(1):
        nodo=nuevo()
        dinstancias=[]
        for i in range(len(optenidos)):
            s=optenidos[i]
            prueba=math.sqrt(math.pow(nodo[0]-s[0],2)+math.pow(nodo[1]-s[1],2))
            dinstancias.append(prueba)
        euler=min(dinstancias)
        pos_arreglo=dinstancias.index(euler)
        #costo
        punto_rect=calculo_Costo(costo,optenidos,nodo,dinstancias,pos_arreglo)
        #esta la meta cerca?
        distancia_meta=math.sqrt(math.pow(c_final[0]-nodo[0],2)+math.pow(c_final[1]-nodo[1],2))
        #das
        base=optenidos[punto_rect]
        nuevo_costo=costo[punto_rect]
        #aquie va los obstaculos
        
        #/////////////////////      falta colocar los obstaculos
        choque=secciones(base,nodo,campo)
        if choque==1:
            costo.append(nuevo_costo+1)
            optenidos.append(nodo)
            if distancia_meta<=radio_b:
                costo.append(nuevo_costo+2)
                optenidos.append(c_final)
                break
    # ruta &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  optenidos
    costo_nodo=costo[len(costo)-1]
    ruta_inve=[c_final]
    nodo_acutal=c_final
    while(1):
        distancia_p=9999999999999999999.99
        if costo_nodo==0:
            return ruta_inve[::-1]
            break
        for i in range(len(costo)):
            test_c=costo[i]
            test_po=optenidos[i]
            distancia_n=math.sqrt(math.pow(test_po[0]-nodo_acutal[0],2)+math.pow(test_po[1]-nodo_acutal[1],2))
            s=secciones(nodo_acutal,test_po,campo)
            if test_c==costo_nodo-1 and distancia_n<distancia_p and s==1:
                distancia_p=distancia_n
                posicion=i
        nodo_acutal=optenidos[posicion]
        ruta_inve.append(nodo_acutal)
        costo_nodo=costo_nodo-1

def optimisar(trayectoria,campo):
    new_trayectoria=[trayectoria[0]]
    prueba_ruta=trayectoria[::-1]
    cont=0
    cont2=0
    final=trayectoria[len(trayectoria)-1]
    while(1):
        nodo=new_trayectoria[cont]
        if nodo==final:
            return new_trayectoria
        for i in range(len(trayectoria)):
            nodo_meta=prueba_ruta[i]
            obstaculo=secciones(nodo,nodo_meta,campo)
            if obstaculo==1:
                new_trayectoria.append(nodo_meta)
                break
        cont=cont+1


## Comados $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
ruta=rrt(campo,radio_a,radio_b,inicio,final)
print(ruta)
dibujo(ruta)
print("Ruta optimizada")
new_ruta=optimisar(ruta,campo)
print(new_ruta)
dibujo2(new_ruta)




