"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from website.views import sitemap, temp, aboutus, adduser, home, service, testalbum, testshow, mail, show, adminfix, adminadd, adminmain, login, logout, albumphoto, albumshow, album, hire, test
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home),
    path('aboutus/', aboutus),
    path('mail/', mail),
    path('service/', service),
    path('hire/', hire),
    path('favicon.ico', RedirectView.as_view(url='/static/myicon.icon')),
    path('captcha/', include('captcha.urls')),
    path('showImg/', show),
    path('adduser/', adduser),
    path('album/', album),
    path('sitemap.xml',sitemap),
    path('home/sitemap.xml',sitemap),
    path('albumshow/<int:albumid>/', albumshow),
    path('albumphoto/<int:photoid>/<int:albumid>/', albumphoto),
    path('home/google2a22239a6a17d4a6.html', temp),
    path('google2a22239a6a17d4a6.html', temp),
    path('test/', test),
    path('testshow/<int:filename>/<int:filenum>/',testshow),
    path('testalbum/<int:fileid>/<int:pictureid>/',testalbum),
    path('login/', login),
    path('logout/', logout),
    path('adminmain/', adminmain),
    path('adminmain/<int:albumid>/', adminmain),
    path('adminadd/', adminadd),
    path('adminfix/<int:albumid>/', adminfix),
    path('adminfix/<int:albumid>/<int:photoid>/', adminfix),
    path('adminfix/<int:albumid>/<int:photoid>/<str:deletetype>/', adminfix),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)