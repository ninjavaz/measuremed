from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('doctor/', views.doctor, name='doctor'),
    path('patient/', views.patient, name='patient'),
    path('create-measure/', views.createMeasure, name="create-measure"),
    path('delete-measure/<str:pk>', views.deleteMeasure, name="delete-measure"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

]   


