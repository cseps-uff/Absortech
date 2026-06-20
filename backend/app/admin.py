from django.contrib import admin
from .models import Dispenser, LeituraSensor

@admin.register(Dispenser)
class DispenserAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'instituicao',
        'bloco',
        'andar',
        'ativo',
        'created_at'
    )

    list_filter = ('ativo', 'instituicao', 'bloco', 'andar')
    search_fields = ('nome', 'localizacao', 'instituicao', 'bloco')


@admin.register(LeituraSensor)
class LeituraSensorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dispenser',
        'timestamp',
        'distancia_cm',
        'quantidade_estimada',
        'porcentagem_ocupacao'
    )

    list_filter = ('dispenser__instituicao', 'dispenser__bloco')
    search_fields = ('dispenser__nome',)
    readonly_fields = ('quantidade_estimada', 'porcentagem_ocupacao')
