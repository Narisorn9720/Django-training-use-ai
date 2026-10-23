from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a task title',
                'autofocus': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add details about this task',
                'rows': 3,
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'status': 'Status',
        }
