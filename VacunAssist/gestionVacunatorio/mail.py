from email import message
import smtplib



def sendSecondFactor(secondFactor,email,name):
    message="Hola {}, Le agradecemos que se haya registrado en nuestra pagina, Este es el segundo factor para su inicio de sesion: {} ".format(name,secondFactor)
    subject="WolfTech: Envio de segundo factor"
    ms="Subject:{}\n\n{}".format(subject,message)
    server= smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("tobias77aj@gmail.com","")
    server.sendmail("tobias77aj@gmail.com",email,ms)
    server.quit()

def sendchangePassword(email,name):
    message="Hola {}, le informamos que su clave a sido modificada con exito".format(name)
    subject="WolfTech: Cambio de Clave"
    ms="Subject:{}\n\n{}".format(subject,message)
    server= smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("tobias77aj@gmail.com","")
    server.sendmail("tobias77aj@gmail.com",email,ms)
    server.quit()
