# -*- coding: utf-8 -*-

import pickle
import shelve
import telebot 
from telebot import types
import pymysql.cursors

#Get the dates from the document datos.txt
datos = open('datos.txt', 'r')
User = datos.readline().split(";")[1].strip()
Pass = datos.readline().split(";")[1].strip()
TOKEN = datos.readline().split(";")[1].strip() # This is the TOKEN that BotFather give us
datos.close()

#Make the needed conections
bot = telebot.TeleBot(TOKEN) # Make our Bot Object
conection = pymysql.connect(host = '127.0.0.1', user = 'root' , password = '' ,db = 'FinalFantasy', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor) #Connect Python with our Data Base
cur = conection.cursor() 

#This method read all the messages than bot get

def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
            cid = m.chat.id # Almacenaremos el ID de la conversación.
            print ("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.

#Search in to database writing the WHERE statement Splitting the line jump in this form :
#/buscar
#WHERE statement etc
@bot.message_handler(commands = ['buscar'])
def busqueda(m):
	lista = m.text.split("\n")

	try:
		consulta = 'SELECT * FROM Carta ' + lista[1]
		print (consulta)
		if cur.execute(consulta) == 0:
			bot.send_message(m.chat.id, 'No se ha encontrado ninguna coincidencia en la base de datos')
			return

		print ('consulta realizada')
		for row in cur:
			bot.send_message(m.chat.id,printC(row))

	except Exception :
			bot.reply_to(m, 'El texto introducido no es un formato valido en MySQL')

#This method make the complete str than bot send us
def printC(row):
	cadena = ""

	if row['Tipo'] == 'Delantero':
		cadena = "Nombre - EX - Cantidad Campo : " + row['Nombre'] + " - " + str(row['Ex']) + " - " + str(row['Campo']) + "\nCoste , Elemento: [" + str(row['Coste']) + ", " + row['Elemento'] + "]" + "\nTipo / Oficio / Categoria : " + row['Tipo'] + " / " + row['Oficio'] + " / " + row['Categoria'] + '\nTexto:\n'+ row['Texto'] +"\nPoder : " + str(row['Poder']) + "\nSerie : " + row['ID_Sobre'] + "-" + row['ID_Carta'] + row['Rareza']
	if row['Tipo'] == 'Apoyo':
		cadena = "Nombre - EX - Cantidad Campo : " + row['Nombre'] + " - " + str(row['Ex']) + " - " + str(row['Campo']) + "\nCoste , Elemento: [" + str(row['Coste']) + ", " + row['Elemento'] + "]" + "\nTipo / Oficio / Categoria : " + row['Tipo'] + " / " + row['Oficio'] + " / " + row['Categoria'] + '\nTexto:\n'+ row['Texto'] + "\nSerie : " + row['ID_Sobre'] + "-" + row['ID_Carta'] + row['Rareza']
	if row['Tipo'] == u'Invocación':
		cadena = "Nombre - EX : " + row['Nombre'] + " - " + str(row['Ex']) + "\nCoste , Elemento: [" + str(row['Coste']) + ", " + row['Elemento'] + "]" + "\nTipo / Categoria : " + row['Tipo'] + " / " + row['Categoria'] + '\nTexto:\n'+ row['Texto'] + "\nSerie : " + row['ID_Sobre'] + "-" + str(row['ID_Carta']) + row['Rareza']
	print (cadena)
	
	return cadena

#Comand for Isntert element in the data base
@bot.message_handler(commands = ['insert'])
def insert(m):
	lista = m.text.split(" ")
	insercion = 'INSERT INTO Carta VALUES(' + lista[1] + ", "+ lista[2] + ", "+ lista[3] + ", "+ lista[4] + ", "+ lista[5] + ", "+ lista[6] + ", "+ lista[7] + ", "+ lista[8] + ", "+ lista[9] + ", "+ lista[10] + ", "+ lista[11] + ", "+ lista[12] + ", "+ lista[13] + ");"
	try:
		cur.execute(insercion)
		conection.commit()
	except Exception:
		bot.reply_to(m, 'No ha sido posible la insercion de elemento')

#insert a complete MYSQL Script
@bot.message_handler(commands = ['mysql'])
def mysql(m):
	lista = m.text.split("\n")
	try:
		if cur.execute(lista[1]) == 0:
			bot.send_message(m.chat.id, 'No se ha encontrado ninguna coincidencia en la base de datos')
			return

		salida = ""
		for row in cur:
			for el in row:
				print(salida)
				salida = salida + el + ": " 
				print(salida)
				if(type(row[el]) == unicode):
					salida = salida+ row[el] +"\n"
				else:
					salida = salida + str(row[el]) + "\n"
			bot.send_message(m.chat.id, salida)
	except Exception:
		bot.reply_to(m, 'El texto introducido no es un formato valido en MySQL ó ha habido un probema con la operación')

#delete an element from Data Base
@bot.message_handler(commands = ['delete'])
def delete(m):
	lista = m.text.split('\n')
	datos = lista[1].split('-')
	cadena = 'DELETE FROM Carta WHERE ID_Sobre = ' + str(atos[0]) + ' AND ID_Carta = ' + datos[1] 
	try:
		cur.execute(cadena)
		conection.commit()
	except:
		bot.reply_to(m, ' No se ha podido realizar la eliminacion')

#Search a element by Name, Category, Type, Ofice, if is EX, or element
@bot.message_handler(commands = ['Nombre','Categoria','Tipo','Oficio', 'Ex', 'Elemento'])
def busquedaAvanzada(m):
	lista = m.text.split(' ')

	cadena = 'SELECT * FROM Carta WHERE ' + lista[0][1:] + ' = ' + lista[1]
	print (cadena)

	try:
		if cur.execute(cadena) == 0:
			bot.reply_to(m, "No se ha encontrado coincidencias en la base de datos")
			return

		for row in cur:
			bot.send_message(m.chat.id, printC(row))

	except Exception:
		bot.reply_to(m, 'El texto introducido no es un formato valido en MySQL ó ha habido un probema con la operación' )

#Search a element by Power or Cost
@bot.message_handler(commands = ['Poder','Coste'])
def busquedaAvanzadaNum(m):
	lista = m.text.split(' ')
	cadena = ''
	try:
		a = int(lista[1])
		b = int(lista[2])

		if a > b:
			a,b = b,a

		cadena = 'SELECT * FROM Carta WHERE ' + lista[0][1:] + ' BETWEEN ' + str(a) + ' AND ' + str(b)

	except Exception:
		
		cadena ='SELECT * FROM Carta WHERE ' + lista[0][1:] + ' ' + lista[1] + ' ' + lista[2]

	print(cadena) 

	try:
		print(cadena)
		if cur.execute(cadena) == 0:
			bot.reply_to(m, "No se ha encontrado coincidencias en la base de datos")
			return

		for row in cur:
			bot.send_message(m.chat.id, printC(row))

	except Exception:
		bot.reply_to(m, 'El texto introducido no es un formato valido en MySQL ó ha habido un probema con la operación' )

#Search a element by Series
@bot.message_handler(commands = ['Serie'])
def busquedaSerie(m):
	lista = m.text.split(' ')
	cadena = 'SELECT * FROM Carta WHERE ID_Sobre = ' + lista[1] + ' AND ID_Carta = ' + lista[2]
	print(cadena)
	
	try:
		if cur.execute(cadena) == 0:
			bot.reply_to(m, "No se ha encontrado coincidencias en la base de datos")
			return

		for row in cur:
			bot.send_message(m.chat.id, printC(row))

	except Exception:
		bot.reply_to(m, 'El texto introducido no es un formato valido en MySQL ó ha habido un probema con la operación' )

#Search a element by Stock
@bot.message_handler(commands = ['Cantidad'])
def busq_cant(m):
	lista = m.text.split(' ')
	cadena = 'SELECT * FROM Carta WHERE ID_Carta = ' + lista[1]
	print(cadena)

	try:
		if cur.execute(cadena) == 0:
			bot.reply_to(m, "No se ha encontrado coincidencias en la base de datos")
			return
		for row in cur:
			bot.reply_to(m, 'Posees :' + str(row['Cantidad']) )

	except Exception:
		bot.reply_to(m, 'El texto introducido no es un formato valido en MySQL ó ha habido un probema con la operación' )

#Change the Stock in the DB
@bot.message_handler(commands = ['setc'])
def setCant(m):
	lista = m.text.split(' ')
	consulta = 'SELECT Cantidad FROM Carta WHERE ID_Sobre = '+ lista[1] + ' AND ID_Carta = ' + lista[2]
	try:
		if(cur.execute(consulta) == 0):
			bot.reply_to(m, "No se ha encontrado coincidencias en la base de datos")
			return
		
		for row in cur:
			cantidad = row['Cantidad']
		
		cantidad = int(lista[3]) + cantidad
		cur.execute('UPDATE Carta SET Cantidad = '+ str(cantidad) +' WHERE ID_Sobre ='+ lista[1]+' AND ID_Carta = "001"')
		conection.commit()
	except Exception :
		bot.reply_to(m, 'El texto introducido no es un formato valido use [/Comando ID_Sobre ID_Carta Cantidad]' )

bot.polling(none_stop=True)