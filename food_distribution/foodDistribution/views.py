from collections import defaultdict
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import *

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
            elif profile.user_type == "manager":
                return redirect('managerDashboard')
            elif profile.user_type == "donor":
                return redirect('monetaryDonation')
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

            #Logs the user in
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

@login_required(login_url = "login")
def managerDashboard(request):
    foodDonation = FoodDonation.objects.all()
    food_stock = FoodStock.objects.all()
    food_types = [stock.food_type for stock in food_stock]
    food_quantity = [int(stock.quantity) for stock in food_stock]


    foods  = Food.objects.order_by('created_at')                     # 1 :contentReference[oaicite:4]{index=4}
    unique_dates = sorted({f.created_at for f in foods})                   # 2 :contentReference[oaicite:5]{index=5}

    temp = defaultdict(lambda: {d: 0 for d in unique_dates})              # 3 :contentReference[oaicite:6]{index=6}
    for f in foods:
        temp[f.food_type][f.created_at] += float(f.quantity)

    stock_series = {                                                     # 4 :contentReference[oaicite:7]{index=7}
        ft: [temp[ft][d] for d in unique_dates]
        for ft in temp
    }
<<<<<<< HEAD
    date_labels = [d.strftime('%Y-%m-%d') for d in unique_dates]

=======

    # Convert dates to string format for JSON serialization
    date_labels = [date.strftime('%Y-%m-%d') for date in dates]

    units = 0
    #Calculate the total units of stock
    for donation in foodDonation:
        units = units + int(donation.quantity)
>>>>>>> 557a19d2974ba4fecab970c6cff5f42b8ad02aa0
    
    context = {
        'user_profile': Profile.objects.get(user = request.user),
        'food_types': food_types,
        'food_quantity': food_quantity,
        'dates': date_labels,
        'stock_series': stock_series,
        'food_donation': foodDonation,
        'units': units,
    }


   
    return render(request, 'managerDashboard.html', context)


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

@login_required(login_url = "login")
def monetaryDonation(request):
    if request.method == 'POST':
        username = request.POST.get('donor_name')  
        profile = Profile.objects.get(user =request.user)  
        try:
            md = MonetaryDonation.objects.get(donor=profile)
            md.donation_amount += Decimal(request.POST['donation_amount'])
            md.save()
        except MonetaryDonation.DoesNotExist:
            MonetaryDonation.objects.create(
                donor=profile,
                donation_amount=request.POST['donation_amount'],
                payment_method=request.POST['donation_method']
            )
        return redirect('monetaryDonation')
    return render(request, 'monetary_donation.html')



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
    food = Food.objects.all()

    food_name = [name.food_name for name in food]
    food_quantity = [int(name.quantity) for name in food]
    food_items = zip(food_name, food_quantity)
    context = {
        'user_profile': Profile.objects.get(user = request.user),
        'food_name': food_name,
        'food_quantity': food_quantity,
        'food_items': food_items
    }
    return render(request, 'stock_monitoring.html', context)

def assignVolunteers(request):
    template = loader.get_template('assignVolunteers.html')
    return HttpResponse(template.render())

@login_required(login_url = "login")
def foodDonation(request):
    if request.method == 'POST':
        food_type = request.POST.get('food-type')
        food_name = request.POST['food-name']
        expiry_date = request.POST.get('expire-date')
        quantity = request.POST['quantity']
        storage_location = request.POST['storage-location']

        #Create a food donation
        new_foodDonation = FoodDonation.objects.create(donor = Profile.objects.get(user = request.user), food_type = food_type, quantity = int(quantity), expiry_date = expiry_date)
        new_foodDonation.save()

        #Try to get the food name that already exists
        try:
            new_food = Food.objects.get(food_name = food_name)
            new_food.quantity = new_food.quantity + int(quantity)
            new_food.save()
        
        #creates a new food
        except Food.DoesNotExist:
            new_food = Food.objects.create(food_name = food_name, food_type = food_type, expire_date = expiry_date, quantity = quantity, storage_location = storage_location)
            new_food.save()

        #adds the new food according to the food_type
        try:
            food_stock = FoodStock.objects.get(food_type=food_type)

        # Update the quantity
            food_stock.quantity = food_stock.quantity + int(quantity)  # Increment the quantity
            food_stock.save()  # Save the updated food stock instance
            return redirect('foodDonation')
    
        except FoodStock.DoesNotExist:
            # If FoodStock does not exist, create a new record
            food_stock = FoodStock(food_type=food_type, quantity=new_food.quantity)
            food_stock.save()  # Save the new food stock instance
            return redirect('foodDonation')
    else:
        return render(request, 'Food_Donation.html')