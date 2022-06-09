from encodings import search_function
from msilib.schema import Class
from django.contrib import admin

from gestionVacunatorio.models import *

# Register your models here.


#class ClientAdmin(admin.ModelAdmin):
 #   list_display=("name","surname","dni","dateOfBirth","zone","email","genre")
  #  list_filter=("name","surname","dni","email","zone")
   # search_field=("name","surname","dni","email","zone")

class VaccinatortAdmin(admin.ModelAdmin):
    list_display=("name","surname","dni","email")
    list_filter=("name","surname","dni","email")

class UserAdmin(admin.ModelAdmin):
    list_display=("name","surname","dni","dateOfBirth","zone","email","gender")
    list_filter=("name","surname","dni","email","zone")
    search_field=("name","surname","dni","email","zone")

class AdminAdmin(admin.ModelAdmin):
    list_display=("name","is_admin")
    list_filter=("name","is_admin")


#class FormularyAdmin(admin.ModelAdmin):
  #  list_display=("user","risk","admissionDate")
   # list_filter=("name","risk","admissionDate")

#class VaccineAdmin(admin.ModelAdmin):
 #   list_display=("name","timeSpan")
   # list_filter=("name","timeSpan")

#class VaccineAdmin(admin.ModelAdmin):
 #   list_display=("formulary","vaccine","doseNumber","aplicationDate")
  #  list_filter=("formulary","vaccine","doseNumber","aplicationDate")

#class TurnAdmin(admin.ModelAdmin):
 #   list_display=("user","vaccine","status","date")
  #  list_filter=("user","vaccine","status","date")

#class ForumAdmin(admin.ModelAdmin):
 #   list_display=("user","title","description","date")
  #  list_filter=("user","title","description","date")


admin.site.register(Vaccinator,VaccinatortAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Admin,AdminAdmin)
#admin.site.register(Formulary,FormularyAdmin)
#admin.site.register(Vaccine,VaccineAdmin)
#admin.site.register(Turn,TurnAdmin)
#admin.site.register(Forum,ForumAdmin)



