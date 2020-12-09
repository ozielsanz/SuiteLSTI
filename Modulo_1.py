from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email, smtplib, ssl
import logging
import nmap


def enviar_correos(sender_mail,receiver_mail,subject,body,password):
    try:
        message = MIMEMultipart()
        message["From"] = sender_mail
        message["To"] = receiver_mail
        message["Subject"] = subject
        message["Bcc"] = body  
        message.attach(MIMEText(body, "plain"))
            
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_mail, password)
            server.sendmail(sender_mail, receiver_mail, subject, body)
    except Exception as e:
        logging.error("Ha ocurrido un error: " + str(e))
        return "Ha ocurrido un error: " + str(e)
        

def escanear_puertos(begin,end):
    ips_up = []
    target = '192.168.100.62/24'
    try:
        scanner = nmap.PortScanner()
        scanner.scan(target,str(begin)+"-"+str(end))
        for host in scanner.all_hosts():
            for i in range(begin,end+1):
                    if scanner[host]['tcp'][i]['state'] == 'open':
                        ips_up.append(scanner[host]['addresses']['ipv4'])

        for ip in ips_up:
            scanner.scan(str(ip),str(begin)+"-"+str(end))
            f = open('scaneolocaldered.csv','a')
            f.write(scanner.csv())
            f.close()
    except Exception as e:
        logging.error("Ha ocurrido un error: " + str(e))
        return "Ha ocurrido un error: " + str(e)
        



