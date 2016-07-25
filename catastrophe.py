#!/usr/bin/env python
__author__      = "rsanchezav"

import re
import pdb
import pandas as pd
import requests
import urllib2
from lxml import html
from bs4 import BeautifulSoup
import socks
import socket
import urllib2
from TorCtl import TorCtl

class query_catastro(object):
	"""
	sudo pip install -U selenium
	sudo pip install pyvirtualdisplay
	sudo apt-get install xvfb

	How to use it:

	import catastrophe	
	#instanciate class - This function prepares the application and assigns a valid cookie
	
	model = catastrophe.query_catastro()	
	
	#Having done that you are ready to search for a lat/long
	
	catastro = model.get_account(19.401408,-99.201958)
	
	#You will receive a pandas DF with zoning and land use information from SEDUVI:
	#CuentaCatastral: |latitud: |longitud: |Delegacion: |Uso del Suelo 1: |Niveles: 
	#|Altura: |Zrea Libre: |M2 min. Vivienda: |Densidad: 
	#|Superficie Maxima de Construccion (Sujeta a restricciones*): |Numero de Viviendas Permitidas:
	"""

	def prepare_to_request_account(self,LAT,LON):
		ENDPOINT="/busquedageoseduvi/buscarCuentaCatastral"
		url=self.ROOT_URL + ENDPOINT

		# Parameters
		url+="?"
		url+="&xScreen=" + str(self.MOUSE_CLICK_X)
		url+="&yScreen=" + str(self.MOUSE_CLICK_Y)
		url+="&x=" + str(LON)
		url+="&y=" +  str(LAT)
		url+="&z=0"
		url+="&mapWidth=" + str(self.MAP_WIDTH)
		url+="&mapHeight=" + str(self.MAP_HEIGHT)
		url+="&ocultar=1"

		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 'JSESSIONID=' + self.SESSION_COOKIE))
		f = opener.open(url)


	def get_account(self,LAT,LON):

		self.prepare_to_request_account(LAT,LON)
		
		ENDPOINT="/principalMapFrameActualizar.jsp"
		url=self.ROOT_URL + ENDPOINT

		# Parameters
		url+="?"

		url+="&op=-1"
		url+="&x=" + str(LON)
		url+="&y=" + str(LAT)
		url+="&z=1"
		url+="&mapWidth=" + str(self.MAP_WIDTH)
		url+="&mapHeight=" + str(self.MAP_HEIGHT)
		url+="&dir=0"
		url+="&xMouseDown=" + str(self.MOUSE_CLICK_X)
		url+="&yMouseDown=" + str(self.MOUSE_CLICK_Y)
		url+="&xMouseUp=" + str(self.MOUSE_CLICK_X)
		url+="&yMouseUp=" + str(self.MOUSE_CLICK_Y)
		url+="&stepZoom=2"
		url+="&verEscala=1"
		url+="&verVistaAerea=1"
		url+="&verControles=1"
		url+="&xVistaAerea=0"
		url+="&yVistaAerea=0"
		url+="&zVistaAerea=0"
		url+="&setStar=0"
		url+="&sizeVistaAerea=150"
		url+="&topStarGuardado=0"
		url+="&leftStarGuardado=0"
		url+="&displayLayerGuardado=none"
		url+="&topLayerGuardado=0"
		url+="&leftLayerGuardado=0"
		url+="&widthLayerGuardado=0"
		url+="&heightLayerGuardado=0"
		url+="&mapImage=MapStreamServlet\?x=" + str(LON)
		url+="&y=" + str(LAT)
		url+="&z=1.0"
		url+="&mapWidth=" + str(self.MAP_WIDTH)
		url+="&mapHeight=" + str(self.MAP_HEIGHT)
		url+="&geosetRutaArchivoPrincipal=D:\\seduvidatos\\cartografia\\Default3.mdf"
		url+="&geosetRutaCarpetaPrincipal=D:\\seduvidatos\\cartografia"
		url+="&recupSession=1"
		url+="&guardarMapa=0"
		url+="&setCopyright=0"
		url+="&xUtm=0"
		url+="&yUtm=0"
		url+="&zFrameVistaAerea=3.0"
		url+="&zMapFrameVistaAerea=1.0"

		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 'JSESSIONID=' + self.SESSION_COOKIE))
		f = opener.open(url)
		text = str(f.read())
		catastro = re.search("[0-9]{3}_[0-9]{3}_[0-9]{2}",text).group(0)	
		delegacion = re.search("c[A-Z][\w+\s\w+]*",text).group(0)
		return catastro, delegacion


	def get_ficha(self,LAT,LON):
		info = self.get_account(LAT,LON)
		print "info reached"

		ENDPOINT="/fichasReporte/fichaInformacion.jsp?"		
		url=self.ROOT_URL + ENDPOINT
		url+="nombreConexion=" + str(info[1])
		url+="&cuentaCatastral=" + str(info[0])
		url+="&idDenuncia=&ocultar=1"
		url+="&x=" + str(LON)
		url+="&y="+ str(LAT)
		url+="&z=0.5" 

		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 'JSESSIONID=' + self.SESSION_COOKIE))
		req = requests.get(url)
		tree = html.fromstring(req.content)
		var = tree.xpath('//th[@class="zon"]/text()')
		ans = tree.xpath('//td[@class="zon"]/text()')
		diccionario_predio = {}

		diccionario_predio["CuentaCatastral"] = str(info[0])
		diccionario_predio["Delegacion"] = str(info[1])
		diccionario_predio["latitud"] = str(LAT)
		diccionario_predio["longitud"] = str(LON)

		for v, a in zip(var[:8],ans[:8]):
			diccionario_predio[v] = a

		#print urllib2.urlopen("http://almien.co.uk/m/tools/net/ip/").read()
		
		data = pd.DataFrame(diccionario_predio.values(), index=diccionario_predio.keys()).transpose()

		return data

	def __init__(self):
		super(query_catastro, self).__init__()
	
		self.ROOT_URL="http://ciudadmx.df.gob.mx:8080/seduvi"
		self.MOUSE_CLICK_X=350
		self.MOUSE_CLICK_Y=400
		self.MAP_WIDTH=700
		self.MAP_HEIGHT=800

		# Tor IP.
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, '127.0.0.1', 9050, True)
		socket.socket = socks.socksocket
		proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
		opener = urllib2.build_opener(proxy_support) 

		#self.conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051)
		#self.proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
		#self.conn.send_signal("NEWNYM")
		#opener = urllib2.build_opener(self.proxy_support) 
		#urllib2.install_opener(opener)
		#print "Changing ip address to"  + str((urllib2.urlopen("http://www.ifconfig.me/ip").read()))

		r = requests.get(self.ROOT_URL)
		if r.status_code == 200:
			self.SESSION_COOKIE = r.cookies.items()[0][1]


