from RRT_ROBOT import *
from csv_reader import map_getter
from math import *
#Aqui se calcula la ruta optima segun los parametros dados
campo=map_getter("map1.csv")
ruta=rrt(campo,100,50,[150,150],[-150,-200])
new_ruta=optimisar(ruta,campo)

#Aqui se tabaja con la ruta para obtener las instrucciones que se le daran al robot
print("Ruta optimizada")
print(new_ruta)

x_comp=0
y_comp=0
turn_angle_degree=0 #given in degrees
turn_angle_radian = 0#given in radian
mag=0
distance= 0
xm=3 #meters by 300 pixels
velx=0
vely=0
Tvel=0
time=0
for i in range(0,len(new_ruta)-1):
	x_comp=new_ruta[i+1][0]-new_ruta[i][0]
	y_comp=new_ruta[i+1][1]-new_ruta[i][1]
	mag =  sqrt(pow(x_comp,2)+pow(y_comp,2))
	distance = (mag*xm)/300 
	turn_angle_degree=atan2(y_comp, x_comp)*(180/pi)
	turn_angle_radian=atan2(y_comp, x_comp)
	velx=cos(turn_angle_radian)*0.377 #measured in m/s
	vely=sin(turn_angle_radian)*0.377 #measured in m/s
	Tvel = sqrt(pow(velx,2)+pow(vely,2))
	time = distance/Tvel
	print(distance,time)








