from django.db import models
from django.utils import timezone

# Create your models here.

class ProjectInfo(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='media/')

    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title


class AlbumModel(models.Model):
    adate = models.DateTimeField(auto_now=True)
    alocation = models.CharField(max_length=200, blank=True, default='')
    atitle = models.CharField(max_length=100, null=False)
    adesc = models.TextField(blank=True, default='')
    def __str__(self):
        return self.alocation

class PhotoModel(models.Model):
    palbum = models.ForeignKey('AlbumModel', on_delete=models.CASCADE)
    # psubject = models.CharField(max_length=100, null=False, default='')
    pdate = models.DateTimeField(auto_now=True)
    pimg = models.ImageField(upload_to='photo/')
    # pimg = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.palbum

