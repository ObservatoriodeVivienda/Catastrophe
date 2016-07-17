#!/usr/bin/env python
__author__      = "rsanchezav"

import urllib2
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver

class query_catastro(object):
	"""
	sudo pip install -U selenium
	sudo pip install pyvirtualdisplay
	sudo apt-get install xvfb

	How to use it:
	import catastrophe
	model = catastrophe.query_catastro()
	catastro = model.get_account(19.401408,-99.201958)

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
		soup = BeautifulSoup(text,'html.parser')
		delegacion = soup.find_all('td')[8].getText()
		cp = soup.find_all('td')[6].getText()
		colonia = soup.find_all('td')[4].getText()
		return catastro, delegacion, cp


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
		print url

		url = "http://ciudadmx.df.gob.mx:8080/seduvi/fichasReporte/fichaInformacion.jsp?nombreConexion=ALVARO OBREGON&cuentaCatastral=037_354&idDenuncia=&ocultar=1&x=-99.201958&y=19.401408&z=0.5"
		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 'JSESSIONID=' + self.SESSION_COOKIE))

		req = requests.get(url).text
		print req
		text = str(req)
		return text




	def __init__(self):
		super(query_catastro, self).__init__()
	
		self.ROOT_URL="http://ciudadmx.df.gob.mx:8080/seduvi"
		self.MOUSE_CLICK_X=350
		self.MOUSE_CLICK_Y=400
		self.MAP_WIDTH=700
		self.MAP_HEIGHT=800

		# We need a cookie to make requests effectively
		display = Display(visible=0, size=(1024, 768))
		display.start()
		driver= webdriver.Firefox()
		driver.get("http://ciudadmx.df.gob.mx:8080/seduvi/")
		self.SESSION_COOKIE = driver.get_cookies()[0].get("value")
