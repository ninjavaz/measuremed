from datetime import timedelta
import math
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm


from .decorators import unauthenticated_user, allowed_users

from .models import *
from .forms import CreateUserForm, MeasureForm


from django.contrib import messages
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


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

    measures = Measure.objects.filter(doctor=doctor)
    measuresAmount = measures.count()

    context = {'route': 'doctor', 'measures': measures, 'measuresAmount': measuresAmount, 'doctor': doctor}

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

    measures = Measure.objects.filter(patient=patient)
    measuresAmount = measures.count()

    
    context = {'route': 'patient', 'measures': measures, 'measuresAmount': measuresAmount, 'patient': patient}

    
    

    return render(request, 'app/patient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def createMeasure(request):
    """
    creating measure by users who are in doctor group
    Args:
        request 

    Returns:
        redirection to doctor page, measure for choosen patient
    """
    form = MeasureForm()
    if request.method == 'POST':
        form = MeasureForm(request.POST)
        if form.is_valid():
            form = form.save()


            current_user = request.user
            doctor = Doctor.objects.get(user=current_user.id)

            measure = Measure.objects.get(id=form.id)
            measure.doctor = doctor
            measure.bmi = round((measure.bodyWeight / ((measure.height/100)**2)), 2)
            measure.save()


            return redirect('/doctor')

    context = {'form': form}
    return render(request, 'app/notification-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def deleteMeasure(request, pk):
    """
    deleting a created earlier measure

    Args:
        request 
        pk 

    Returns:
        redirection to page that confirms deletion of a measure
    """
    measure = Measure.objects.get(id=pk)
    if request.method == "POST":
        measure.delete()
        return redirect('/doctor')

    context = {'measure': measure}
    return render(request, 'app/delete.html', context)


