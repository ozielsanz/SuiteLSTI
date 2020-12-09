from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from lxml import html
from bs4 import BeautifulSoup
from Modulo_1 import enviar_correos, escanear_puertos
from Modulo_2 import metadata_imagenes, web_scraping, mostrar_hostactual, hunterapi
import email, smtplib, ssl
import os
import requests
import nmap
import argparse
import socket
import logging
import subprocess


logging.basicConfig(filename='app.log',level=logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    #Modo
    parser.add_argument('-m','--modo', type=int, help="Opcion del menu a realizar: \n1-Envio de correos, \n 2-Escaneo de puertos, \n \n 3-Metadata de imagenes, \n 4-Web Scrapping, \n 5-Uso de Hunter para correos web, \n 6-Mostrar host actual, \n 7-Obtener hashes de una ruta")        

    #Envio de correos
    parser.add_argument('-s',"--subject",type=str, help='Asunto del email')
    parser.add_argument('-b','--body', type=str, help='Cuerpo del  email')
    parser.add_argument('-sm','--sendermail', type=str, help='Emisor of the email')
    parser.add_argument('-rm','--receivermail', type=str, help='Receptor del  email')
    parser.add_argument('-p','--password', type=str, help='Password del email')
    
    #Escaneo de puertos
    parser.add_argument('-be','--begin', type=int, help='Indica el puerto inicial')
    parser.add_argument('-en','--end', type=int, help='Indica el puerto final')

    #Metadata de imagenes
    parser.add_argument('-r','--ruta', type=str, help='Indica la ruta de las imagenes')
    
    #WebScraping
    parser.add_argument('-u','--url', type=str, help='Indica la URL a investigar')
    parser.add_argument('-bu','--busqueda', type=int, help='Indica que deseas buscar en la pagina: 1 IMAGENES, 2 PDFS, 3 LINKS')
    parser.add_argument('-api', type=str, help='APIKEY de Hunter')
    parser.add_argument('-tmp','--tempfile',help ='Indica el nombre del archivo donde se guardaran los hashes')
    params = parser.parse_args()
    



if params.modo == 1:
    body = params.body
    subject = params.subject
    receiver_mail = params.receivermail
    sender_mail = params.sendermail
    password = params.password
    enviar_correos(sender_mail,receiver_mail,subject,body,password)

elif params.modo == 2:
    end = params.end
    begin = params.begin
    escanear_puertos(begin,end)

elif params.modo == 3:
    ruta = params.ruta
    metadata_imagenes(ruta)

elif params.modo == 4:
    busqueda = params.busqueda
    url = params.url
    web_scraping(busqueda,url)

elif params.modo == 5:
    url = params.url
    api = params.api
    hunterapi(url, api)

elif params.modo == 6:
    mostrar_hostactual()


elif params.modo == 7:
    ruta = params.ruta
    targetPath = ruta
    tmpFile = "Hashes.txt"
    command = "powershell -ExecutionPolicy ByPass -File HashAcquire.ps1 -TargetFolder "+\
                  targetPath + " -ResultFile " + tmpFile 
    powerShellResult = subprocess.run(command, stdout=subprocess.PIPE)
