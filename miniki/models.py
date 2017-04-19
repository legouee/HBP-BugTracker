from django.db import models
from django.core.urlresolvers import reverse

import uuid

class Ctx (models.Model):
    collab = models.CharField(max_length=1024) 
    ctx = models.CharField(max_length=1024) 

    def as_json(self):
        return {
            'collabe': self.collab,
            'ctx': self.ctx
        }

class Project(models.Model):                   
    """A Project"""

    title = models.CharField(max_length=1024)
    # ctx = models.UUIDField(unique=True)

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
        return reverse('project-list' ) #, args=[str(self.ctx)])


class Ticket(models.Model):                   
    """A Ticket"""
    ctx = models.ForeignKey(Ctx, on_delete=models.CASCADE, default = 0)
    title = models.CharField(max_length=1024)
    text = models.TextField(help_text="formatted using ReST")
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, default="")
    author = models.CharField(max_length=200,default="")

    def __unicode__(self):
        return self.title
    # UUIDField is not supported by automatic JSON serializer
    # so we add a method that retrieve a more convenient dict.
    def as_json(self):
        return {
            'title': self.title,
            'text': self.text,
            'status': self.status,
            'author': self.author,
            'ctx': self.ctx,
        }

    @models.permalink
    def get_absolute_url(self):
        return reverse('ticket_list' )#, args=[str(self.ctx)])
    @models.permalink
    def get_absolute_url():
        return reverse('ticket_list' )


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, default = 0)
    author = models.CharField(max_length=200, default="")
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
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
            'author': self.author
        }


