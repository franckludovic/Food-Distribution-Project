from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('privacyPolicy', views.privacyPolicy, name='privacyPolicy'),
    path('termsAndConditions', views.termsAndConditions, name='termsAndConditions'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('adminDashboard', views.adminDashboard, name='adminDashboard'),
    path('beneficiaryProfile', views.beneficiaryProfile, name='beneficiaryProfile'),
    path('volunteerProfile', views.volunteerProfile, name='volunteerProfile'),
    path('collectionPointsManagement', views.collectionPointsManagement, name='collectionPointsManagement'),
    path('confirmationPage', views.confirmationPage, name='confirmationPage'),
    path('foodAidRequest', views.foodAidRequest, name='foodAidRequest'),
    path('foodDistributionPlanning', views.foodDistributionPlanning, name='foodDistributionPlanning'),
    path('foodStockManagement', views.foodStockManagement, name='foodStockManagement'),
    path('monetaryDonation', views.monetaryDonation, name='monetaryDonation'),
    path('notifications', views.notifications, name='notifications'),
    path('onlineSupport', views.onlineSupport, name='onlineSupport'),
    path('reportsAnalytics', views.reportsAnalytics, name='reportsAnalytics'),
    path('settings', views.settings, name='settings'),
    path('stockMonitoring', views.stockMonitoring, name='stockMonitoring'),
    path('assignVolunteers', views.assignVolunteers, name='assignVolunteers'),
]