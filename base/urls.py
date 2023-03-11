from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name="login"), #we can use this name='login' instead of providing url anywhere in code
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('', views.home,name="home"),
    path('room/<str:pk>/', views.room,name="room"),
    path('profile/<str:pk>/',views.userProfile,name='user-profile'),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"), #str pk as we need to pass primary key to upate room function
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),

]