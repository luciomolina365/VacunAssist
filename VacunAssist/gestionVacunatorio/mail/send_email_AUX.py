import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


texte = f'''
    Bonjour 
    Ma super newsletter
    Cdt
    mon_lien_incroyable
    '''

html = f'''
<html>
<body>
<h1>Bonjour</h1>
<p>Ma super newsletter</p>
<b>Cdt</b>
<br>
<a href="https://datascientest.com">mon_lien_incroyable</a>
</body>
</html>
'''
def send_secondFactor_mail(email_receiver, name,secondFactor):
  html = f'''
    <html>
    <body>
    <h1>Hola{name}</h1>
    <br>
    <h1>Bonjour</h1>
    <br>
    </body>
    </html>'''
  pass


def send_mail(email_receiver, messageSubject, texte, html ):
  
  smtp_address = 'smtp.gmail.com'
  smtp_port = 465


  email_address = 'example@gmail.com'
  email_password = 'my_password'


  message = MIMEMultipart("alternative")
  message["Subject"] = messageSubject
  message["From"] = email_address
  message["To"] = email_receiver


  texte_mime = MIMEText(texte, 'plain')
  html_mime = MIMEText(html, 'html')


  message.attach(texte_mime)
  message.attach(html_mime)

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:

    server.login(email_address, email_password)

    server.sendmail(email_address, email_receiver, message.as_string())