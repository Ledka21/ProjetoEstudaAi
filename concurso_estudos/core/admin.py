from django.contrib import admin
from .models import Concurso, Materia, Topico, MetaEstudo, SessaoEstudo

@admin.register(Concurso)
class ConcursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'banca', 'data_prova', 'usuario')
    list_filter = ('banca',)
    search_fields = ('nome', 'banca')

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'area', 'peso', 'status', 'concurso', 'usuario')
    list_filter = ('status', 'area', 'concurso')
    search_fields = ('nome', 'area')

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'materia', 'status', 'ultima_revisao', 'proxima_revisao')
    list_filter = ('status', 'materia')
    search_fields = ('nome',)

@admin.register(MetaEstudo)
class MetaEstudoAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'horas_objetivo', 'materia', 'ativa', 'usuario')
    list_filter = ('periodo', 'ativa')
    list_editable = ('ativa',)

@admin.register(SessaoEstudo)
class SessaoEstudoAdmin(admin.ModelAdmin):
    list_display = ('data', 'materia', 'topico', 'duracao_minutos', 'tipo', 'produtividade')
    list_filter = ('data', 'tipo', 'produtividade', 'materia')
    search_fields = ('anotacoes',)
    date_hierarchy = 'data'