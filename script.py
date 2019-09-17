#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
    @Descripción: Este programa extrae y guarda en formato csv los registros
    publicados en la pagina web www.cafextremadura.es/listado-colegiados
    @Autor: Manuel Parra
    @Licencia: MIT
    @Fecha: 14/09/2019
    @Modificado: 14/09/2019
"""
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import nettest
import ssl
import sys
import csv

# test our Internet connection
print("Testing the Internet connection, please wait!")
host = ['8.8.8.8', '8.8.4.4']
nt = nettest.chargetest(host)

if not nt.isnetup():
    print("Your Internet connection is down!!, try leter again!")
    exit()

print("The Internet connection is ok!")

# ignore SSL certificate
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


url = "http://www.cafextremadura.es/listado-colegiados"

# get data
print("Retrieving data from", url + ", please wait...")
try:
    data = urllib.request.urlopen(url, context=ctx)
except Exception as err:
    print("Error to retrieve the url", err)
    quit()

try:
    html = data.read()
except Exception as err:
    print("Error to read data from", url, err)
    quit()

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table')

ths = soup.find_all('th')
theaders = []
for th in ths:
    if len(th) == 1:
        theaders.append(th.contents[0].strip())
        theaders.append('Estatus')
    if len(th) == 3:
        theaders.append(th.contents[0].strip())
        theaders.append(th.contents[2].strip())

trs = soup.find_all('tr')
trows = []
trows.append(theaders)
for tr in trs:
    tcs = []
    tds = tr.find_all('td')
    for td in tds:
        if len(td) == 5:
            nombre = td.find('strong')
            if nombre != None:
                tcs.append(nombre.contents[0].strip())
                tcs.append(td.contents[4].strip())
                name = None
                continue
            mail = td.find('span')
            if mail != None:
                tcs.append(td.contents[0].strip())
                if len(mail):
                    tcs.append(mail.contents[0].strip())
                mail = None
        if len(td) == 3:
            tcs.append(td.contents[0].strip())
            tcs.append(td.contents[2].strip())
    if tcs == []: continue
    trows.append(tcs)

fname = "registros.csv"
print("Escribiendo los datos en el archivo", fname)
with open('files/'+fname, 'w') as file:
    write = csv.writer(file)
    write.writerows(trows)

print("Proceso finalizado!")
