import datetime
import requests
import time
import RPi.GPIO as GPIO
import time
from datetime import date
import datetime
from time import sleep


# to spam the pygame.KEYDOWN eve
now = datetime.datetime.now()
last = datetime.datetime.now()

in1 = 8 # Salida al rele
in2 = 10 # Entrada del sensor de nivel

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.IN)
GPIO.output(in1, True)

global vectorRiego 
global vectorPendientes 
vectorRiego = [[14.44, 1], [14.47, 1]]
vectorPendientes = []

def guardarVector(hora, tiempo):
	vectorRiego.append([hora, tiempo])
	print(vectorRiego)

def sendChange(param):
	myobj = {'id': param}
	x = requests.post(URL+'change', data = myobj)
	print(x.status_code)
	sleep(1)
	
def guardar_pendiente():
	for i in range(len(vectorRiego)):
		vectorActual = vectorRiego[i]
		horaMinActual = vectorActual[0]
		horaActual = int(str(horaMinActual).split('.')[0])
		minutoActual = int(str(horaMinActual).split('.')[1])
		tiempoActual = int(vectorActual[1])
			
		if now.hour ==  horaActual and now.minute == minutoActual:
			vectorPendientes.append([horaActual, minutoActual, tiempoActual])
			print("Guardando riego pendiente de las " + str(horaActual) + ":" + str(minutoActual))
			time.sleep(60)
			
def regar_pendiente():
	global vectorPendientes
	print(vectorPendientes)
	print("Regando pendientes")
	if len(vectorPendientes) > 0:
		for i in range (len(vectorPendientes)):
			tiempoActual = vectorPendientes[i][2]
			GPIO.output(in1, False)
			print("Riego pendiente " + str(i) + " On")
			time.sleep(60*tiempoActual)
			GPIO.output(in1, True)
			print("Riego pendiente Off")
		vectorPendientes = []
	else:
		print("No hay pendientes")
	

def estadoTanque():
	
	print("Sensando nivel de agua")
	state = 'No hay agua'
	cont = 0
	for i in range (20):
		cont = cont + (GPIO.input(10))
		sleep(0.5)
		
	if cont < 1:
		state = 'Hay agua'
		
	return state
	
	
def regar():	
	print("Riego normal")
	for i in range(len(vectorRiego)):
		vectorActual = vectorRiego[i]
		horaMinActual = vectorActual[0]
		horaActual = int(str(horaMinActual).split('.')[0])
		minutoActual = int(str(horaMinActual).split('.')[1])
		tiempoActual = int(vectorActual[1])
		print(vectorActual)
		if now.hour ==  horaActual and now.minute == minutoActual:
			GPIO.output(in1, False)
			print("Riego On")
			time.sleep(60*tiempoActual)
			print("Riego Off")
			GPIO.output(in1, True)

try:
	while True:
		now = datetime.datetime.now()
		dia = datetime.datetime.today()
		print("-"*60)
		print(now)
		state_tanque = estadoTanque()
		if state_tanque == 'Hay agua':
			print(state_tanque)
			regar_pendiente()
			regar()
		else:
			print(state_tanque)
			guardar_pendiente()
			
			
except KeyboardInterrupt, ValueError:
	GPIO.cleanup()
	
		
