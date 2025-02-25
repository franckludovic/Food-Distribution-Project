from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render())

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

def beneficiaryProfile(request):
    template = loader.get_template('beneficiary_profile.html')
    return HttpResponse(template.render())

def volunteerProfile(request):
    template = loader.get_template('volunteer_profile.html')
    return HttpResponse(template.render())

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

def stockMonitoring(request):
    template = loader.get_template('stock_monitoring.html')
    return HttpResponse(template.render())