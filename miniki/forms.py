from django import forms
from .models import TicketPage, HomePage, TicketPageCreate

class TicketPageForm(forms.ModelForm):
    """Ticket Page edition form"""

    class Meta:
        model = TicketPage
        fields = ['title', 'text'] #, 'ctx']
        widgets = {
            # 'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'TicketPage.title',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control form-control-editor',
                'ng-model': 'TicketPage.text',
            }),
        }

class TicketCreationPageForm(forms.ModelForm):
    """Ticket Page creation form"""

    class Meta:
        model = TicketPageCreate
        fields = ['title', 'text','created_by'] #, 'ctx']
        widgets = {
            # 'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'create_ticket_Page.title',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'ng-model': 'create_ticket_Page.text',
            }),
            'created_by': forms.HiddenInput(),  
        }     

class HomePageForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = ['title'] #, 'ctx']
        widgets = {
            # 'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'HomePage.title',
            })
        }


#class ticketListForm ?
