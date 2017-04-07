from django import forms
#from .models import TicketPage 
from .models import Ticket
from .models import Home


#class TicketPageForm(forms.ModelForm): 
class TicketForm(forms.ModelForm):           
    """Ticket edition form"""

    class Meta:
        #model = TicketPage
        model = Ticket
        fields = ['title', 'text', 'ctx']
        widgets = {
            'ctx': forms.HiddenInput(),
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

# class ProjectForm(forms.ModelForm):
#     """Ticket Page edition form"""

#     class Meta:
#         model = Home
#         fields = ['project_name', 'ctx']
#         widgets = {
#             'ctx': forms.HiddenInput(),
#             'project_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'ng-model': 'Home.priject_name',
#             }),
#         }  

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['project_name', 'ctx']
        widgets = {
            'ctx': forms.HiddenInput(),
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'Home.project_name',
            })
        }

