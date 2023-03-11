
from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    path('admin/', admin.site.urls), #default admin panel
    path('',include('base.urls')),
]
