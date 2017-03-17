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

from miniki.views import show, edit, config, home

from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^$', 'miniki.views.show', name='wiki_page_show'),
#     url(r'^edit/$', 'miniki.views.edit', name='wiki_page_edit'),
# ]

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'miniki.views.show', name='wiki_page_show'),
    # url(r'^edit/$', 'miniki.views.edit', name='wiki_page_edit'),


    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('hbp_app_python_auth.urls', namespace='hbp-social')),

    url(r'^$', show, name='ticket_page_show'),
    url(r'^edit/$', edit, name='ticket_page_edit'),
    url(r'^home/$', home, name='home_page'),
    

    #url(r'^config.json$', 'miniki.views.config', name='config'),
    url(r'^config.json$', config, name='config'),
    

    
]