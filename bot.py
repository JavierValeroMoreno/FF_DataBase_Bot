# -*- coding: utf-8 -*-

import pickle
import shelve
import telebot 
from telebot import types
import pymysql.cursors


datos = open('datos.txt', 'r')
User = datos.readline().split(";")[1].strip()
Pass = datos.readline().split(";")[1].strip()

print (User)
print (Pass)

conection = pymysql.connect(host = '127.0.0.1', user = 'root' , password = '' ,db = 'FinalFantasy', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
cur = conection.cursor()


TOKEN = datos.readline().split(";")[1].strip() # Nuestro tokken del bot (el que @BotFather nos dió).
bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.

def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
            cid = m.chat.id # Almacenaremos el ID de la conversación.
            print ("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.

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

@bot.message_handler(commands = ['queinsertar'])
def duda(m):
	cid = m.chat.id

	bot.send_message(cid, 'El formato de insercion es: ID_Sobre(varchar), ID_Carta(int), Nombre(varchar), Coste(Int), Elemento(varchar), Campo(int), Ex(Bool), Tipo (varchar), Oficio(Varchar), Categoria(varchar), Rareza(Varchar), Poder(int), Cantidad(int)')

@bot.message_handler(commands = ['insert'])
def insert(m):
	lista = m.text.split(" ")
	insercion = 'INSERT INTO Carta VALUES(' + lista[1] + ", "+ lista[2] + ", "+ lista[3] + ", "+ lista[4] + ", "+ lista[5] + ", "+ lista[6] + ", "+ lista[7] + ", "+ lista[8] + ", "+ lista[9] + ", "+ lista[10] + ", "+ lista[11] + ", "+ lista[12] + ", "+ lista[13] + ");"
	try:
		cur.execute(insercion)
	except Exception:
		bot.reply_to(m, 'No ha sido posible la insercion de elemento')

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
				salida = salida + el + ": " + str(row[el]) +"\n"
			bot.send_message(m.chat.id, salida)
	except Exception:
		bot.reply_to(m, 'El texto introducido no es un formato valido en MySQL ó ha habido un probema con la operación')

@bot.message_handler(commands = ['delete'])
def delete(m):
	lista = m.text.split('\n')
	datos = lista[1].split('-')
	cadena = 'DELETE FROM Carta WHERE ID_Sobre = ' + str(atos[0]) + ' AND ID_Carta = ' + datos[1] 
	try:
		cur.execute(cadena)
	except:
		bot.reply_to(m, ' No se ha podido realizar la eliminacion')

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

bot.polling(none_stop=True)