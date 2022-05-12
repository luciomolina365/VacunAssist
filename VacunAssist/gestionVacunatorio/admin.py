from encodings import search_function
from msilib.schema import Class
from django.contrib import admin

from gestionVacunatorio.models import Client, Vaccinator

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display=("name","surname","dni","dateOfBirth","zone","email")
    list_filter=("name","surname","dni","email","zone")
    search_field=("name","surname","dni","email","zone")

class VaccinatortAdmin(admin.ModelAdmin):
    list_display=("name","surname","dni","email")
    list_filter=("name","surname","dni","email")


admin.site.register(Client,ClientAdmin)
admin.site.register(Vaccinator,VaccinatortAdmin)
