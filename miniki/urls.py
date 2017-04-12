"""miniki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include

# from miniki.views import show_ticket
from miniki.views import config
from miniki.views import HomeView
# from miniki.views import edit_ticket
from miniki.views import CreateTicketView#create_ticket
from miniki.views import create_project
from miniki.views import TicketListView

from miniki.views import Test_Menu_deroulant

from miniki.views import TicketDetailView
from miniki.views import ProjectListView




from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('hbp_app_python_auth.urls', namespace='hbp-social')),

    #url(r'^show_ticket/$', show_ticket, name='ticket_page_show'),
    # url(r'^show_ticket/$', show_ticket, name='ticket_show'),
    #url(r'^edit_ticket/$', edit_ticket, name='ticket_page_edit'),
    # url(r'^edit_ticket/$', edit_ticket, name='ticket_edit'),
    #url(r'^create_ticket/$', create_ticket, name='ticket-create'), #create_ticket/
    url(r'^create_ticket/$', CreateTicketView.as_view(), name='ticket-create'), #create_ticket/
    url(r'^Menu_deroulant$', Test_Menu_deroulant, name='Menu_deroulant'), 
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^project_list/$',ProjectListView.as_view(), name='project-list'),
    url(r'^create_project/$', create_project, name='project-create'),
    #url(r'^ticket_list/(?P<pk>\d+)/$',TicketListView.as_view(), name='ticket-list2'),
    url(r'^ticket_list/$',TicketListView.as_view(), name='ticket-list'),


    # url(r'^ticket_detail/$',TicketDetailView.as_view(), name='ticket-detail'),

    # url(r'^ticket_detail/(?P<ticket_id>.*)/$', TicketDetailView.as_view(), name="ticket-detail"),

    # url(r'^(?P<slug>[-\w]+)/$', TicketDetailView.as_view(), name='ticket-detail'),
    # url(r'^(?P<pk>\d+)/$', TicketDetailView.as_view(), name='ticket-detail'),
    url(r'^ticket/(?P<pk>\d+)/$', TicketDetailView.as_view(), name='ticket-detail'),

    url(r'^config.json$', config, name='config'),
    
]