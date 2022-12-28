from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('doctor/', views.doctor, name='doctor'),
    path('patient/', views.patient, name='patient'),
    path('create-notification/', views.createNotification, name="create-notification"),
    path('delete-notification/<str:pk>', views.deleteNotification, name="delete-notification"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

]   


