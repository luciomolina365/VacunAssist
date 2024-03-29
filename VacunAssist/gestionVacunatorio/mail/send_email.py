from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(email_receiver, messageSubject, texte, html ):

  smtp_address = 'smtp.gmail.com'
  smtp_port = 465


  email_address = 'wolftech.contacto@gmail.com'
  #email_password = 'quiquewolff'
  email_password = 'nvtllybnhbnoyfza'

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


def send_secondFactor_email(email_receiver, name, secondFactor):
  html = f'''
  <html>
  <body>
  <h3>Hola {name}, le agradecemos que se haya registrado en nuestra pagina. Este es el segundo factor para su inicio de sesion: </h3>
  <br>
  <h1>{secondFactor} </h1>
  <br>
  </body>
  </html>'''
  texte =f'''
  Hola{name}, le agradecemos que se haya registrado en nuestra pagina. Este es el segundo factor para su inicio de sesion:   
  {secondFactor}
  '''
  send_mail(email_receiver, 'VacunAssist - Segundo Factor', texte, html)


def send_passwordConfirm_email(email_receiver, name):
    html = f'''
    <html>
    <body>
    <h3>Hola {name}, le informamos que su clave a sido modificada con exito.</h3>
    <br>
    </body>
    </html>'''
    texte =f'''
    Hola {name}, le informamos que su clave a sido modificada con exito.
    '''
    send_mail(email_receiver, 'VacunAssist - Clave Modificada', texte, html)

def send_turnCancelation_email(email_receiver, name):
    html = f'''
    <html>
    <body>
    <h3>Hola {name}, le informamos que su solicitud de turno para vacuna de fiebre amarilla fue denegada.</h3>
    <br>
    </body>
    </html>'''
    texte =f'''
    Hola {name}, le informamos que su solicitud de turno para vacuna de fiebre amarilla fue denegada.
    '''
    send_mail(email_receiver, 'VacunAssist - Solucitud denegada', texte, html)

def send_password_email(email_receiver, name, password):
  html = f'''
  <html>
  <body>
  <h3>Hola {name}, ha sido registrado como vacunador. Le informamos que su clave es </h3> <h1>{password} </h1>.
  <br>
  </body>
  </html>'''
  texte =f'''
  Hola {name}, ha sido registrado como vacunador. Le informamos que su clave es {password} .
  '''
  send_mail(email_receiver, 'VacunAssist - Clave Modificada', texte, html)

def send_turn_confirmation_email(email_receiver, name, zone, date ):
  html = f'''
  <html>
  <body>
  <h3>Hola {name}, su solicitud para la vacuna de la fiebre amallida fue confirmada.  </h3>
  <h3>Su turno será el día {date.day}/{date.month}/{date.year} en el vacunatorio de zona {zone}. </h3>
  <br>
  <br>
  </body>
  </html>'''
  texte =f'''
  Hola {name}, su solicitud para la vacuna de la fiebre amallida fue confirmada.
  Su turno será el día {date.day}/{date.month}/{date.year} en el vacunatorio de zona {zone}.
  '''

  send_mail(email_receiver, 'VacunAssist - Confirmación de turno fiebre amarilla.', texte, html)
#send_secondFactor_email('yo.y.mis.videos@gmail.com', 'Lucio', 666)
#send_passwordConfirm_email('tobias77aj@gmail.com', 'Tobi, paraguayo')

#send_turn_confirmation_email('lucio_molina_365@live.com', 'Lucio', 'Menemlandi', datetime.today() )