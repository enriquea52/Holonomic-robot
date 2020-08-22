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

def nuevo(Ra_ro):
    x=randint(-300+Ra_ro, 300-Ra_ro);
    y=randint(-300+Ra_ro, 300-Ra_ro);
    return[x,y]

def prueba (punto,area):
    x_obstaculos=[]
    y_obstaculos=[]
    for i in range(len(area)):
        j=area[i]
        if punto[0]>=j[0] and punto[0]<=(j[0]+j[2]) and punto[1]>=j[1] and punto[1]<=(j[1]+j[3]):
            return 0
    return 1

def dibuja_obstaculo(matriz,radio):
    for i in range(len(matriz)):
        objeto=matriz[i]
        x_0=objeto[0]+radio;y_0=objeto[1]+radio;x_F=objeto[2]-2*radio;y_F=objeto[3]-2*radio;
        flecha.begin_fill()
        flecha.goto(x_0,y_0)
        flecha.pendown()
        flecha.goto(x_0+x_F,y_0)
        flecha.goto(x_0+x_F,y_0+y_F)
        flecha.goto(x_0,y_0+y_F)
        flecha.goto(x_0,y_0)
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

def calculo_Costo(costo,puntos,nodo,distancia,posicion,radio_a):
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




#Busqueda &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def rrt(campo,radio_a,radio_b,c_inicio,c_final,Ra_ro):
    optenidos=[c_inicio]
    costo=[0]
    while(1):
        nodo=nuevo(Ra_ro)
        dinstancias=[]
        for i in range(len(optenidos)):
            s=optenidos[i]
            prueba=math.sqrt(math.pow(nodo[0]-s[0],2)+math.pow(nodo[1]-s[1],2))
            dinstancias.append(prueba)
        euler=min(dinstancias)
        pos_arreglo=dinstancias.index(euler)
        #costo
        punto_rect=calculo_Costo(costo,optenidos,nodo,dinstancias,pos_arreglo,radio_a)
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





