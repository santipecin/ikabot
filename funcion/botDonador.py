#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import traceback
from config import *
from helpers.botComm import *
from helpers.pedirInfo import *
from helpers.process import forkear
from helpers.gui import enter
from helpers.signals import setInfoSignal
from helpers.getJson import getCiudad
from helpers.recursos import getRecursosDisponibles

def botDonador(s):
	if botValido(s) is False:
		return
	print('¿Donar a aserraderos o a bienes de cambio? [a/b]')
	rta = read(values=['a', 'A', 'b', 'B'])
	tipo = 'resource' if rta.lower() == 'a' else 'tradegood'
	print('Se donará compulsivamente cada día.')
	enter()

	forkear(s)
	if s.padre is True:
		return

	info = '\nDono todos los días\n'
	setInfoSignal(s, info)
	(idsCiudades, ciudades) = getIdsDeCiudades(s)
	ciudades_dict = {}
	for idCiudad in idsCiudades:
		html = s.get(urlCiudad + idCiudad)
		ciudad = getCiudad(html)
		ciudades_dict[idCiudad] = ciudad['islandId']
	try:
		while True:
			for idCiudad in idsCiudades:
				html = s.get(urlCiudad + idCiudad)
				madera = getRecursosDisponibles(html)[0]
				idIsla = ciudades_dict[idCiudad]
				s.post(payloadPost={'islandId': idIsla, 'type': tipo, 'action': 'IslandScreen', 'function': 'donate', 'donation': madera, 'backgroundView': 'island', 'templateView': 'resource', 'actionRequest': s.token(), 'ajax': '1'})
			time.sleep(24*60*60)
	except:
		msg = 'Ya no se donará.\n{}'.format(traceback.format_exc())
		sendToBot(s, msg)
		s.logout()
