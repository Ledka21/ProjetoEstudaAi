from django import forms
from .models import Concurso, Materia, Topico, Subtopico, MetaEstudo, SessaoEstudo

class ConcursoForm(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = ['nome', 'banca', 'data_prova']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: TJ-SP 2026'}),
            'banca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Vunesp'}),
            'data_prova': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nome', 'area', 'peso', 'status', 'concurso']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Direito Constitucional'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Direito'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'concurso': forms.Select(attrs={'class': 'form-control'}),
        }

class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ['nome', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Princípios Fundamentais'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SubtopicoForm(forms.ModelForm):
    class Meta:
        model = Subtopico
        fields = ['nome', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Art. 5º - Direitos Individuais'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SessaoEstudoForm(forms.ModelForm):
    class Meta:
        model = SessaoEstudo
        fields = ['data', 'materia', 'topico', 'duracao_minutos', 'tipo', 'produtividade', 'anotacoes']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'materia': forms.Select(attrs={'class': 'form-control'}),
            'topico': forms.Select(attrs={'class': 'form-control'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 60 (minutos)'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'produtividade': forms.Select(attrs={'class': 'form-control'}),
            'anotacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Anotações da sessão...'}),
        }

class MetaEstudoForm(forms.ModelForm):
    class Meta:
        model = MetaEstudo
        fields = ['periodo', 'horas_objetivo', 'materia', 'ativa']
        widgets = {
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'horas_objetivo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'Ex: 4.0'}),
            'materia': forms.Select(attrs={'class': 'form-control'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }