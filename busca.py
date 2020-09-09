# !/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: iso-8859-1
# encoding: win-1252

import urllib.request
from unicodedata import normalize
from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify

obj = Flask(__name__)


def extrair_palavras(content):
	soup = BeautifulSoup(content, "html.parser")
	lista_sinonimos = soup.find_all('a', class_='sinonimo')
	sinon = []

	if len(lista_sinonimos) == 0:
		return None

	for lista_sin in lista_sinonimos:
		x = str(normalize('NFKD', lista_sin.next_element).encode('ASCII', 'ignore').decode('ASCII'))
		sinon.append(x)
		print(x)

	return sinon


@obj.route('/<sinonimo>')
@cross_origin()
def busca_palavra(sinonimo):

	sin = normalize('NFKD', sinonimo).encode('ASCII', 'ignore').decode('ASCII')

	try:
		html = urllib.request.urlopen('https://www.sinonimos.com.br/' + sin + '/').read()
		html = str(html)

		return jsonify(extrair_palavras(html))

	except:
		return "Nao foi encontrado sinonimo para [" + sin + "]"


obj.run(port=5002)
