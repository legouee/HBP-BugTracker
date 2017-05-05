from django import forms

from .models import Ticket
from .models import Comment
from .models import Project


class TicketForm(forms.ModelForm):           
    """Ticket edition form"""

    class Meta:
        model = Ticket
        fields = ['title', 'text' ]
        widgets = {

            'id_projet': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'Ticket.title',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control form-control-editor',
                'ng-model': 'Ticket.text',
            }),

        }  

class ProjectForm(forms.ModelForm):
    """Ticket Page edition form"""

    class Meta:
        model = Project
        fields = ['title' ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'Project.title',
            }),
        }  


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text',]

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'ng-model': 'Comment.text',
            })
        }
        