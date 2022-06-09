from datetime import date, timedelta

class Turn():
    user  = None
    vaccine = None
    status = False
    date = None
    
    def __init__(self,vaccine, date) -> None:
        pass

class UserDDD():
    datos = None


def asignar_turno_covid(edad,de_riesgo, cant_dosis_dadas):

    if edad < 18:
        raise ValueError("No deberia asignar un turno(COVID) a un menor de 18")

    if cant_dosis_dadas != None: #solicitar nro de dosis aplicadas al modelo
        dias = 0
        rango_edades = list(range(18,61))
        usuario = UserDDD()
        vacuna = "consulta a la bbdd" 
        fecha = date.today()

        if cant_dosis_dadas == 0:
            if (edad in rango_edades and de_riesgo) or edad > 60:
                dias = 7                    
                fecha = fecha.__add__(timedelta(dias))
   
                Turn(vacuna,fecha)
                return "Asignar turno exitoso"
            if edad in rango_edades and not de_riesgo:
                dias = 21                 
                fecha = fecha.__add__(timedelta(dias))

                Turn(vacuna,fecha)
                return "Asignar turno exitoso"

        if cant_dosis_dadas == 1:
            fechaDosisAnterior = date.today() #consulta a la bbdd
            fechaDosisAnterior = fechaDosisAnterior.__add__(timedelta(22))
            hoy = date.today()

            if fecha.__add__(timedelta(21)).__gt__(date.today()): #si ya pasaron 21 dias
                pass
                return "Asignar turno exitoso"

        if cant_dosis_dadas == 2:
            return "YA tiene las dos dosis"

    return 1

       
       
asignar_turno_covid(45,True, 1)  

