from django.db import models
from django.core.urlresolvers import reverse

import uuid

#class TicketPage(models.Model): 
class Ticket(models.Model):                   
    """A Ticket"""

    title = models.CharField(max_length=1024)
    text = models.TextField(help_text="formatted using ReST")
    # This field stores the UUID added as an argument by the Collaboratory.
    # ctx = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    ctx = models.UUIDField(unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    id_project =  models.IntegerField(default=0) #models.ForeignKey('Project', default=1)#, on_delete=models.CASCADE())
    status = models.IntegerField(default=0) 
    # created_by = models.IntegerField()

    def __unicode__(self):
        return self.title
    # UUIDField is not supported by automatic JSON serializer
    # so we add a method that retrieve a more convenient dict.
    def as_json(self):
        return {
            'title': self.title,
            'text': self.text,
            'ctx': str(self.ctx),
            'id_project': self.id_project,
            'status': self.status,
            #'created_by': self.created_by
        }

    @models.permalink
    def get_absolute_url(self):
        return reverse('ticket-show', args=[str(self.ctx)])

class Project(models.Model):                   
    """A Project"""

    title = models.CharField(max_length=1024)
    ctx = models.UUIDField(unique=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    # UUIDField is not supported by automatic JSON serializer
    # so we add a method that retrieve a more convenient dict.
    def as_json(self):
        return {
            'title': self.title,
        }
    @models.permalink
    def get_absolute_url(self):  
        return reverse('project-list', args=[str(self.ctx)])

class Comment(models.Model):
    # use_name = models.CharField(max_length=1024)
    text = models.TextField(help_text="formatted using ReST")
    ctx = models.UUIDField(unique=True)

    def as_json(self):
        return {
            'text': self.text,
            'ctx': str(self.ctx),
            #'created_by': self.created_by
        }

    @models.permalink
    def get_absolute_url(self):
        return reverse('ticket_show', args=[str(self.ctx)])

class Home(models.Model):
    # ctx = models.UUIDField(unique=True, default=uuid.uuid4, editable=True ) #, unique=True was at primary_key=True spot,   # editable=False)
    #id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4(), editable=True ) #bytes="abcdefghijklmno"
    # print ("Home ctx : ")
    # print (ctx) # ok probleme ici..... peut etre pour ca que ctx = None .....

    project_name = models.CharField(max_length=1024) 
    ctx = models.UUIDField(unique=True)

    def __unicode__(self):
        return self.project_name

    def as_json(self):
        return {
            'project_name': self.project_name,
            'ctx': str(self.ctx),
        }

    @models.permalink
    def get_absolute_url(self):
        return reverse('home', args=[str(self.ctx)])
    
