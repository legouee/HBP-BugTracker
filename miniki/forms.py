from django import forms
from .models import TicketPage, WellcomePage

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
                'ng-model': 'ticketPage.text',
            }),
        }


class WellcomePageForm(forms.ModelForm):
    class Meta:
        model = WellcomePage
        fields = ['title', 'ctx']
        widgets = {
            'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'WellcomePage.title',
            })
        }


#class ticketListForm ?
