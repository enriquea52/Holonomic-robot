from turtle import *
from random import seed
from random import randint
import turtle
import math

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def dibuja_obstaculo(matriz):
    for i in range(len(matriz)):
        if i==0:
            flecha.color("blue")
        elif i==1:
            flecha.color("green")
        elif i==2:
            flecha.color("red")
        elif i==3:
            flecha.color("orange")
        elif i==4:
            flecha.color("black")
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
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
tipo=input("Elija el tipo de mapa, segun su numero(1,2,3,4): ")
print("caja a)= Azul")
print("caja b)= Verde")
print("caja c)= Rojo")
print("caja d)= Naranja")
print("caja e)= Negro")

print(tipo)
setup(700,700, 0, 0)
screensize(600, 600)
title("Mapas")

window = turtle.Screen()
flecha = turtle.Turtle()
flecha.hideturtle()
flecha.penup()
flecha.goto(-300,-300)
flecha.speed(60)
flecha.pendown()
flecha.pensize(3)
for i in range(4):
    flecha.forward(600)
    flecha.left(90)
flecha.penup()
flecha.pensize(0)

mapa=[]
if tipo=="1":
    mapa=[[-23,47,87,54],[-67,27,44,74],[-66,-38,63,63],[-5,-100,71,39],[-67,-100,62,62]]
elif tipo=="2":
    mapa=[[-150,-87,67,87],[106,74,44,74],[-150,-150,63,63],[35,111,71,39],[-87,-150,62,62]]
elif tipo=="3":
    mapa=[[-100,-33,54,67],[-100,-105,74,72],[-26,-105,63,63],[-100,34,39,71],[37,-105,62,62]]
elif tipo=="4":
    mapa=[[130,96,87,54],[-50,106,74,44],[60,-130,63,63],[-200,111,71,39],[-110,-130,62,51]]
else:
    mapa=[]



dibuja_obstaculo(mapa)

turtle.mainloop()


