from django.db import models
from django.core.urlresolvers import reverse

import uuid

#class TicketPage(models.Model): 
class Ticket(models.Model):                   
    """A Ticket"""
    # comments = models.ForeignKey(Comment)
    title = models.CharField(max_length=1024)
    text = models.TextField(help_text="formatted using ReST")
    # This field stores the UUID added as an argument by the Collaboratory.
    # ctx = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    # ctx = models.UUIDField(unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    id_project = models.ForeignKey('Project', on_delete=model.CASCADE())
    # created_by = models.IntegerField()

    def __unicode__(self):
        return self.title
    # UUIDField is not supported by automatic JSON serializer
    # so we add a method that retrieve a more convenient dict.
    def as_json(self):
        return {
            'title': self.title,
            'text': self.text,
            # 'ctx': str(self.ctx),

            'id_project': self.id_project

            #'created_by': self.created_by
        }

    @models.permalink
    def get_absolute_url(self):
        return reverse('ticket_show' )#, args=[str(self.ctx)])

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
    # ticket = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    # null=True
    # pub_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def as_json(self):
        return {
            'text': self.text,
            #'ctx': str(self.ctx),
            #'created_by': self.created_by
        }



class Home(models.Model):
    # ctx = models.UUIDField(unique=True, default=uuid.uuid4, editable=True ) #, unique=True was at primary_key=True spot,   # editable=False)
    #id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4(), editable=True ) #bytes="abcdefghijklmno"
    # print ("Home ctx : ")
    # print (ctx) # ok probleme ici..... peut etre pour ca que ctx = None .....

    project_name = models.CharField(max_length=1024) 
    # ctx = models.UUIDField(unique=True)

    def __unicode__(self):
        return self.project_name

    def as_json(self):
        return {
            'project_name': self.project_name,
            # 'ctx': str(self.ctx),
        }

    @models.permalink
    def get_absolute_url(self):
        return reverse('home') #, args=[str(self.ctx)])
    
