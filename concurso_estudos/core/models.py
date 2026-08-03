from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Concurso(models.Model):
    """Representa um concurso público que o usuário está prestando."""
    nome = models.CharField('Nome do Concurso', max_length=200)
    banca = models.CharField('Banca', max_length=100, blank=True)
    data_prova = models.DateField('Data da Prova', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Concurso'
        verbose_name_plural = 'Concursos'
        ordering = ['data_prova']

    def __str__(self):
        return self.nome

class Materia(models.Model):
    """Uma matéria de estudo (ex: Direito Constitucional)."""
    STATUS_CHOICES = [
        ('nao_iniciado', 'Não Iniciado'),
        ('em_andamento', 'Em Andamento'),
        ('revisado', 'Revisado'),
        ('dominado', 'Dominado'),
    ]

    nome = models.CharField('Nome', max_length=200)
    area = models.CharField('Área', max_length=100, blank=True)
    peso = models.IntegerField('Peso', default=1, help_text='Importância da matéria (1-10)')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='nao_iniciado')
    concurso = models.ForeignKey(Concurso, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def total_minutos_estudados(self):
        """Soma de minutos de todas as sessões desta matéria."""
        return sum(s.duracao_minutos for s in self.sessoes.all())

class Topico(models.Model):
    """Um tópico dentro de uma matéria (ex: Princípios Fundamentais)."""
    STATUS_CHOICES = [
        ('nao_estudado', 'Não Estudado'),
        ('em_andamento', 'Em Andamento'),
        ('revisado', 'Revisado'),
        ('dominado', 'Dominado'),
    ]

    nome = models.CharField('Nome', max_length=300)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='nao_estudado')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='topicos')
    ultima_revisao = models.DateField('Última Revisão', null=True, blank=True)
    proxima_revisao = models.DateField('Próxima Revisão', null=True, blank=True)

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.materia.nome} → {self.nome}"

class MetaEstudo(models.Model):
    """Metas de horas de estudo (diária, semanal, mensal)."""
    PERIODO_CHOICES = [
        ('diaria', 'Diária'),
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
    ]

    periodo = models.CharField('Período', max_length=10, choices=PERIODO_CHOICES)
    horas_objetivo = models.DecimalField('Horas Objetivo', max_digits=5, decimal_places=2)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ativa = models.BooleanField('Ativa', default=True)

    class Meta:
        verbose_name = 'Meta de Estudo'
        verbose_name_plural = 'Metas de Estudo'

    def __str__(self):
        return f"{self.get_periodo_display()} - {self.horas_objetivo}h"

class SessaoEstudo(models.Model):
    """Registro de uma sessão de estudo realizada."""
    TIPO_CHOICES = [
        ('teoria', 'Teoria'),
        ('exercicios', 'Exercícios'),
        ('revisao', 'Revisão'),
        ('simulado', 'Simulado'),
    ]
    PRODUTIVIDADE_CHOICES = [
        (1, 'Baixa'),
        (2, 'Média'),
        (3, 'Alta'),
    ]

    data = models.DateField('Data')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='sessoes')
    topico = models.ForeignKey(Topico, on_delete=models.SET_NULL, null=True, blank=True)
    duracao_minutos = models.PositiveIntegerField('Duração (minutos)')
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='teoria')
    anotacoes = models.TextField('Anotações', blank=True)
    produtividade = models.IntegerField('Produtividade', choices=PRODUTIVIDADE_CHOICES, default=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sessão de Estudo'
        verbose_name_plural = 'Sessões de Estudo'
        ordering = ['-data']

    def __str__(self):
        return f"{self.data} - {self.materia.nome} ({self.duracao_minutos}min)"

    @property
    def duracao_horas(self):
        """Retorna a duração formatada em horas."""
        return self.duracao_minutos / 60

class Subtopico(models.Model):
    """Um subtópico dentro de um tópico (ex: Art. 5º - Direitos Individuais)."""
    STATUS_CHOICES = [
        ('nao_estudado', 'Não Estudado'),
        ('em_andamento', 'Em Andamento'),
        ('revisado', 'Revisado'),
        ('dominado', 'Dominado'),
    ]

    nome = models.CharField('Nome', max_length=300)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='nao_estudado')
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='subtopicos')

    class Meta:
        verbose_name = 'Subtópico'
        verbose_name_plural = 'Subtópicos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.topico.nome} → {self.nome}"