from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import Profile, VolunteerProfile

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

@login_required(login_url = "login")
def home(request):
    context = {
        'user_profile': Profile.objects.get(user = request.user)
    }
    return render(request, 'home.html', context)

def login(request):
    
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            profile = Profile.objects.get(user = user)
            if profile.user_type == "volunteer":
                return redirect('volunteerProfile')
            elif profile.user_type == "beneficiary":
                return redirect('beneficiaryProfile')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    
    else:
        return render(request, 'login.html')

def signup(request):
    
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        userType = request.POST.get('checkbox')

        if User.objects.filter(email = email).exists():
            messages.info(request, "Email already exists")
            return redirect('signup')
        elif User.objects.filter(username = username).exists():
            messages.info(request, "Please change your username")
            return redirect('signup')
        else:
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()

            #Logs the user in and redirect to the home page
            user_login = auth.authenticate(username = username, password = password)
            auth.login(request, user_login)

            #Create a new user profile with phone number and user type
            user_model = User.objects.get(username = username)
            new_profile = Profile.objects.create(user = user_model, id_user = user_model.id, phone = phone, user_type = userType)
            new_profile.save()

            return redirect('login')
    else:
        return render(request, 'signup.html')

@login_required(login_url = "login")
def logout(request):
    auth.logout(request)
    return redirect('main')

def forgotPassword(request):
    template = loader.get_template('forgot_password.html')
    return HttpResponse(template.render())

def privacyPolicy(request):
    template = loader.get_template('privacy_policy.html')
    return HttpResponse(template.render())

def termsAndConditions(request):
    template = loader.get_template('terms_conditions.html')
    return HttpResponse(template.render())

def contactUs(request):
    template = loader.get_template('contact_us.html')
    return HttpResponse(template.render())

def adminDashboard(request):
    template = loader.get_template('admin_dashboard.html')
    return HttpResponse(template.render())

@login_required(login_url = "login")
def beneficiaryProfile(request):
    template = loader.get_template('beneficiary_profile.html')
    return HttpResponse(template.render())

@login_required(login_url = "login")
def volunteerProfile(request):
    if request.method == "POST":
        availability = request.POST['availability']
        intervention_area = request.POST['intervention']
        skills = request.POST['skills']

        user_model = request.user
        profile_model = Profile.objects.get(id_user = user_model.id)
        new_volunteer = VolunteerProfile.objects.create(user = profile_model, availability = availability, intervention_area = intervention_area, skills = skills)
        new_volunteer.save()
        return redirect('home')
    else:
        return render(request, 'volunteer_profile.html')

def collectionPointsManagement(request):
    template = loader.get_template('collection_points_management.html')
    return HttpResponse(template.render())

def confirmationPage(request):
    template = loader.get_template('confirmation_page.html')
    return HttpResponse(template.render())

def foodAidRequest(request):
    template = loader.get_template('food_aid_request.html')
    return HttpResponse(template.render())

def foodDistributionPlanning(request):
    template = loader.get_template('food_distribution_planning.html')
    return HttpResponse(template.render())

def foodStockManagement(request):
    template = loader.get_template('food_stock_management.html')
    return HttpResponse(template.render())

def monetaryDonation(request):
    template = loader.get_template('monetary_donation.html')
    return HttpResponse(template.render())

def notifications(request):
    template = loader.get_template('notifications.html')
    return HttpResponse(template.render())

def onlineSupport(request):
    template = loader.get_template('online_support.html')
    return HttpResponse(template.render())

def reportsAnalytics(request):
    template = loader.get_template('reports_analytics.html')
    return HttpResponse(template.render())

def settings(request):
    template = loader.get_template('settings.html')
    return HttpResponse(template.render())

@login_required(login_url = "login")
def stockMonitoring(request):
    context = {
        'user_profile': Profile.objects.get(user = request.user)
    }
    return render(request, 'stock_monitoring.html', context)

def assignVolunteers(request):
    template = loader.get_template('assignVolunteers.html')
    return HttpResponse(template.render())