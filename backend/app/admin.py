from django.contrib import admin
from .models import Dispenser, LeituraSensor

# Registra os modelos para que eles apareçam no painel visual
admin.site.register(Dispenser)
admin.site.register(LeituraSensor)