from django.contrib import admin
from django.urls import path, include, re_path

# from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from myapps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapps.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)