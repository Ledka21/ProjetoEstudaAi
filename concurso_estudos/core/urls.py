from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('materias/', views.lista_materias, name='lista_materias'),
    path('materias/nova/', views.nova_materia, name='nova_materia'),
    path('materias/<int:pk>/editar/', views.editar_materia, name='editar_materia'),
    path('materias/<int:pk>/excluir/', views.excluir_materia, name='excluir_materia'),
    path('sessoes/', views.lista_sessoes, name='lista_sessoes'),
    path('sessoes/nova/', views.nova_sessao, name='nova_sessao'),
    path('metas/', views.lista_metas, name='lista_metas'),
    path('metas/nova/', views.nova_meta, name='nova_meta'),
        # Concursos
    path('concursos/', views.lista_concursos, name='lista_concursos'),
    path('concursos/novo/', views.novo_concurso, name='novo_concurso'),
    path('concursos/<int:pk>/editar/', views.editar_concurso, name='editar_concurso'),
    path('concursos/<int:pk>/excluir/', views.excluir_concurso, name='excluir_concurso'),
    path('logout/', views.logout_view, name='logout'),
        path('concursos/<int:pk>/', views.detalhe_concurso, name='detalhe_concurso'),
    path('materias/<int:pk>/', views.detalhe_materia, name='detalhe_materia'),
    path('topicos/<int:pk>/', views.detalhe_topico, name='detalhe_topico'),

]