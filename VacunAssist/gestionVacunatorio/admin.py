from msilib.schema import Class
from django.contrib import admin
from gestionVacunatorio.models import Client, Vaccinator

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display=("name","surname","dni","dateOfBirth","zone","email")
    search_field=("name","surname")

admin.site.register(Client,ClientAdmin)
admin.site.register(Vaccinator)
