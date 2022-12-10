from django.contrib import admin
from .models import ProjectInfo, AlbumModel, PhotoModel

# Register your models here.

class PostInfo(admin.ModelAdmin):
    list_display = ('id' ,'title', 'pub_date')
    ordering = ('-id',)
    
class AlbumInfo(admin.ModelAdmin):
    list_display = ('id' ,'atitle', 'adate')
    ordering = ('-id',)

admin.site.register(ProjectInfo, PostInfo)
admin.site.register(AlbumModel, AlbumInfo)
admin.site.register(PhotoModel)