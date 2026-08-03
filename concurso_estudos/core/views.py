from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Materia, SessaoEstudo, MetaEstudo, Concurso, Topico
from .forms import MateriaForm, SessaoEstudoForm, MetaEstudoForm
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def dashboard(request):
    """Página principal com resumo dos estudos."""
    usuario = request.user
    hoje = timezone.now().date()

    # Horas estudadas hoje
    sessoes_hoje = SessaoEstudo.objects.filter(usuario=usuario, data=hoje)
    minutos_hoje = sessoes_hoje.aggregate(Sum('duracao_minutos'))['duracao_minutos__sum'] or 0

    # Horas estudadas na semana (últimos 7 dias)
    inicio_semana = hoje - timedelta(days=hoje.weekday())  # Segunda-feira
    sessoes_semana = SessaoEstudo.objects.filter(
        usuario=usuario, data__gte=inicio_semana
    )
    minutos_semana = sessoes_semana.aggregate(Sum('duracao_minutos'))['duracao_minutos__sum'] or 0

    # Meta diária ativa
    meta_diaria = MetaEstudo.objects.filter(usuario=usuario, periodo='diaria', ativa=True).first()
    meta_diaria_minutos = int(meta_diaria.horas_objetivo * 60) if meta_diaria else None

    # Progresso da meta diária
    if meta_diaria_minutos:
        progresso_diario = min((minutos_hoje / meta_diaria_minutos) * 100, 100)
    else:
        progresso_diario = 0

    # Total de minutos por matéria (para gráfico)
    materias_com_horas = []
    for materia in Materia.objects.filter(usuario=usuario):
        minutos = materia.total_minutos_estudados
        if minutos > 0:
            materias_com_horas.append({
                'nome': materia.nome,
                'minutos': minutos,
                'horas': round(minutos / 60, 1),
            })

    # Últimas 5 sessões
    ultimas_sessoes = SessaoEstudo.objects.filter(usuario=usuario).select_related('materia')[:5]

    # Streak (dias consecutivos estudando)
    dias_streak = 0
    dia_atual = hoje
    while SessaoEstudo.objects.filter(usuario=usuario, data=dia_atual).exists():
        dias_streak += 1
        dia_atual -= timedelta(days=1)

    # Total acumulado de horas
    total_minutos = SessaoEstudo.objects.filter(usuario=usuario).aggregate(
        Sum('duracao_minutos')
    )['duracao_minutos__sum'] or 0

    contexto = {
        'minutos_hoje': minutos_hoje,
        'horas_hoje': round(minutos_hoje / 60, 1),
        'minutos_semana': minutos_semana,
        'horas_semana': round(minutos_semana / 60, 1),
        'meta_diaria': meta_diaria,
        'progresso_diario': round(progresso_diario, 1),
        'materias_com_horas': materias_com_horas,
        'ultimas_sessoes': ultimas_sessoes,
        'dias_streak': dias_streak,
        'total_horas': round(total_minutos / 60, 1),
        'total_materias': Materia.objects.filter(usuario=usuario).count(),
    }
    return render(request, 'core/dashboard.html', contexto)

@login_required
def lista_materias(request):
    """Lista todas as matérias do usuário."""
    materias = Materia.objects.filter(usuario=request.user).select_related('concurso')
    return render(request, 'core/materia_list.html', {'materias': materias})

@login_required
def nova_materia(request):
    """Cria uma nova matéria."""
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.usuario = request.user
            materia.save()
            return redirect('core:lista_materias')
    else:
        form = MateriaForm()
    # Filtrar concursos do usuário logado
    form.fields['concurso'].queryset = Concurso.objects.filter(usuario=request.user)
    return render(request, 'core/materia_form.html', {'form': form, 'titulo': 'Nova Matéria'})

@login_required
def editar_materia(request, pk):
    """Edita uma matéria existente."""
    materia = get_object_or_404(Materia, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('core:lista_materias')
    else:
        form = MateriaForm(instance=materia)
    form.fields['concurso'].queryset = Concurso.objects.filter(usuario=request.user)
    return render(request, 'core/materia_form.html', {'form': form, 'titulo': 'Editar Matéria'})

@login_required
def excluir_materia(request, pk):
    """Exclui uma matéria."""
    materia = get_object_or_404(Materia, pk=pk, usuario=request.user)
    if request.method == 'POST':
        materia.delete()
        return redirect('core:lista_materias')
    return render(request, 'core/materia_confirm_delete.html', {'materia': materia})

@login_required
def lista_sessoes(request):
    """Lista todas as sessões de estudo."""
    sessoes = SessaoEstudo.objects.filter(
        usuario=request.user
    ).select_related('materia', 'topico')
    return render(request, 'core/sessao_list.html', {'sessoes': sessoes})

@login_required
def nova_sessao(request):
    """Registra uma nova sessão de estudo."""
    if request.method == 'POST':
        form = SessaoEstudoForm(request.POST)
        if form.is_valid():
            sessao = form.save(commit=False)
            sessao.usuario = request.user
            sessao.save()
            return redirect('core:dashboard')
    else:
        form = SessaoEstudoForm()
    # Filtrar matérias do usuário logado
    form.fields['materia'].queryset = Materia.objects.filter(usuario=request.user)
    form.fields['topico'].queryset = Topico.objects.filter(materia__usuario=request.user)
    return render(request, 'core/sessao_form.html', {'form': form, 'titulo': 'Nova Sessão de Estudo'})

@login_required
def lista_metas(request):
    """Lista todas as metas de estudo."""
    metas = MetaEstudo.objects.filter(usuario=request.user, ativa=True)
    return render(request, 'core/meta_list.html', {'metas': metas})

@login_required
def nova_meta(request):
    """Cria uma nova meta de estudo."""
    if request.method == 'POST':
        form = MetaEstudoForm(request.POST)
        if form.is_valid():
            meta = form.save(commit=False)
            meta.usuario = request.user
            meta.save()
            return redirect('core:lista_metas')
    else:
        form = MetaEstudoForm()
    form.fields['materia'].queryset = Materia.objects.filter(usuario=request.user)
    return render(request, 'core/meta_form.html', {'form': form, 'titulo': 'Nova Meta de Estudo'})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Concurso
from .forms import ConcursoForm

@login_required
def lista_concursos(request):
    concursos = Concurso.objects.filter(usuario=request.user)
    return render(request, 'core/concurso_list.html', {'concursos': concursos})

@login_required
def novo_concurso(request):
    if request.method == 'POST':
        form = ConcursoForm(request.POST)
        if form.is_valid():
            concurso = form.save(commit=False)
            concurso.usuario = request.user
            concurso.save()
            return redirect('core:lista_concursos')
    else:
        form = ConcursoForm()
    return render(request, 'core/concurso_form.html', {'form': form, 'titulo': 'Novo Concurso'})

@login_required
def editar_concurso(request, pk):
    concurso = get_object_or_404(Concurso, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ConcursoForm(request.POST, instance=concurso)
        if form.is_valid():
            form.save()
            return redirect('core:lista_concursos')
    else:
        form = ConcursoForm(instance=concurso)
    return render(request, 'core/concurso_form.html', {'form': form, 'titulo': 'Editar Concurso'})

@login_required
def excluir_concurso(request, pk):
    concurso = get_object_or_404(Concurso, pk=pk, usuario=request.user)
    if request.method == 'POST':
        concurso.delete()
        return redirect('core:lista_concursos')
    return render(request, 'core/concurso_confirm_delete.html', {'concurso': concurso})

from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('core:dashboard')

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

from .models import Subtopico
from .forms import MateriaForm, TopicoForm, SubtopicoForm

@login_required
def detalhe_concurso(request, pk):
    concurso = get_object_or_404(Concurso, pk=pk, usuario=request.user)
    materias = Materia.objects.filter(concurso=concurso, usuario=request.user)

    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.concurso = concurso
            materia.usuario = request.user
            materia.save()
            return redirect('core:detalhe_concurso', pk=concurso.pk)
    else:
        form = MateriaForm()

    return render(request, 'core/concurso_detail.html', {
        'concurso': concurso,
        'materias': materias,
        'form': form,
    })

@login_required
def detalhe_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, usuario=request.user)
    topicos = Topico.objects.filter(materia=materia)

    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.materia = materia
            topico.save()
            return redirect('core:detalhe_materia', pk=materia.pk)
    else:
        form = TopicoForm()

    return render(request, 'core/materia_detail.html', {
        'materia': materia,
        'topicos': topicos,
        'form': form,
    })

@login_required
def detalhe_topico(request, pk):
    topico = get_object_or_404(Topico, pk=pk)
    subtopicos = Subtopico.objects.filter(topico=topico)

    if request.method == 'POST':
        form = SubtopicoForm(request.POST)
        if form.is_valid():
            subtopico = form.save(commit=False)
            subtopico.topico = topico
            subtopico.save()
            return redirect('core:detalhe_topico', pk=topico.pk)
    else:
        form = SubtopicoForm()

    return render(request, 'core/topico_detail.html', {
        'topico': topico,
        'subtopicos': subtopicos,
        'form': form,
    })