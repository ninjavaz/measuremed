from datetime import timedelta
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django_q.models import Schedule
from django_q.tasks import schedule
from .decorators import unauthenticated_user, allowed_users

from .models import *
from .forms import CreateUserForm, NotificationForm


from django.contrib import messages
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

import channels.layers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@unauthenticated_user
def loginPage(request):
    """
    page that performs authorisation of registered person

    Args:
        request 

    Returns:
        rendered html template
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'app/login.html', {'route': 'login'})
    context = {}
    return render(request, 'app/login.html', {'route': 'login'})

@login_required(login_url='login')
def logoutUser(request):
    """
    logout of the logged person
    
    Args:
    
        request 

    Returns:
        login page
    """
    logout(request)
    return redirect('/login')

@unauthenticated_user
def registerPage(request):
    """
    page that provide registration for unregistered persons

    Args:
        request: username, name, surname, e-mail, password and type of group (patient, doctor)

    Returns:
        redirection to login menu
    """
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.refresh_from_db()

            group =  Group.objects.get(name=form.cleaned_data.get('userGroup'))
            firstName = form.cleaned_data.get('firstName')
            lastName = form.cleaned_data.get('lastName')
            
            user.groups.add(group)

            if group.name == 'patient':
                patient = Patient(user=user, firstName=firstName, lastName=lastName)
                patient.save()
            if group.name == 'doctor':
                doctor = Doctor(user=user, firstName=firstName, lastName=lastName)
                doctor.save()
            

            messages.success(request, 'Acccount was created for ' + username)
            return redirect('/login')

    context = {'form': form, 'route': 'register'}
    return render(request, 'app/register.html', context)




@login_required(login_url='login')
def home(request):
    """
    returning to home page

    Args:
        request 

    Returns:
        rendered html template
    """
    # return HttpResponse('Home Page')
    return render(request, 'app/home.html', {'route': 'home'})

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def doctor(request):
    """
    redirection to doctor page when user choosed group "doctor" in registration page

    Args:
        request 

    Returns:
        rendered html page
    """


    current_user = request.user
    doctor = Doctor.objects.get(user=current_user.id)

    notifications = Notification.objects.filter(doctor=doctor)
    notificationsAmount = notifications.count()

    context = {'route': 'doctor', 'notifications': notifications, 'notificationsAmount': notificationsAmount, 'doctor': doctor}

    return render(request, 'app/doctor.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def patient(request):
    """
    redirection to patient page when user choosed group "patient" in registration page

    Args:
        request 

    Returns:
        rendered html page
    """

    
    current_user = request.user
    patient = Patient.objects.get(user=current_user.id)

    notifications = Notification.objects.filter(patient=patient)
    notificationsAmount = notifications.count()

    
    context = {'route': 'patient', 'notifications': notifications, 'notificationsAmount': notificationsAmount, 'patient': patient}

    
    

    return render(request, 'app/patient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def createNotification(request):
    """
    creating notification by users who are in doctor group
    Args:
        request 

    Returns:
        redirection to doctor page, notification for choosen patient
    """
    form = NotificationForm()
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form = form.save()


            current_user = request.user
            doctor = Doctor.objects.get(user=current_user.id)

            notification = Notification.objects.get(id=form.id)
            notification.doctor = doctor
            notification.save()
    

            schedule('app.jobs.scheduleNotification',
                        notification.pk,
                        schedule_type=Schedule.ONCE, 
                        next_run=notification.plannedOnDate
                        )

            return redirect('/doctor')

    context = {'form': form}
    return render(request, 'app/notification-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def deleteNotification(request, pk):
    """
    deleting a created earlier notification

    Args:
        request 
        pk 

    Returns:
        redirection to page that confirms deletion of a notification
    """
    notification = Notification.objects.get(id=pk)
    if request.method == "POST":
        notification.delete()
        return redirect('/doctor')

    context = {'notification': notification}
    return render(request, 'app/delete.html', context)


