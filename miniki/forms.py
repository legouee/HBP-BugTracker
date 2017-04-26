from django import forms

from .models import Ticket

from .models import Comment

from .models import Project


class TicketForm(forms.ModelForm):           
    """Ticket edition form"""

    class Meta:
        model = Ticket
        fields = ['title', 'text' ] #, 'ctx']
        widgets = {

            # 'ctx': forms.HiddenInput(),

            'id_projet': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                #'ng-model': 'TicketPage.title',
                'ng-model': 'Ticket.title',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control form-control-editor',
                #'ng-model': 'TicketPage.text',
                'ng-model': 'Ticket.text',
            }),

            #'created_by': forms.HiddenInput(),
        }  

class ProjectForm(forms.ModelForm):
    """Ticket Page edition form"""

    class Meta:
        model = Project
        fields = ['title' ] #, 'ctx']
        widgets = {
            # 'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'Project.title',
            }),
        }  


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        # fields = ('author', 'text',)
        fields = ['text',]

        widgets = {
            # 'ctx': forms.HiddenInput(),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'ng-model': 'Comment.text',
            })
        }
        