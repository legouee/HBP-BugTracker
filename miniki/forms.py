from django import forms
from .models import TicketPage 
from .models import Home


class TicketPageForm(forms.ModelForm):
    """Ticket Page edition form"""

    class Meta:
        model = TicketPage
        fields = ['title', 'text', 'ctx']
        widgets = {
            'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'TicketPage.title',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control form-control-editor',
                'ng-model': 'TicketPage.text',
            }),
            #'created_by': forms.HiddenInput(),
        }  

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['title', 'ctx']
        widgets = {
            'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'Home.title',
            })
        }


#class ticketListForm ?
