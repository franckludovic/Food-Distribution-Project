from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model

# User = get_user_model()
# # Create your models here.

# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     phone = models.TextField(max_length = 35)
#     user_type = models.TextField(blank = True)
#     id_user = models.IntegerField(default = 0)

#     def _str_(self):
#         return self.user.username


# Extend Django's built-in User model to include a user type and phone number.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('volunteer', 'Volunteer'),
        ('beneficiary', 'Beneficiary'),
        ('donor', 'Donor'),
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='beneficiary')
    
    def str(self):
        return self.username
    

#food model for info about food..
class Food(models.Model):
    food_id = models.IntegerField(default = 0)
    food_name = models.TextField
    food_type = models.TextField (max_length = 50)
    expire_date = models.DateTimeField( auto_now_add=True)
    quantity = models.FloatField(blank= False)
    storage_location = models.TextField(blank= True)

    def _str_(self):
        return self.food_name


# Profile for beneficiaries with extra details.
class BeneficiaryProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='beneficiary_profile')
    number_of_dependents = models.IntegerField(default=0)
    specific_needs = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    
    def str(self):
        return f"{self.user.username} BeneficiaryProfile"

# Profile for volunteers with availability and skills.
class VolunteerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='volunteer_profile')
    availability = models.TextField() 
    intervention_area = models.CharField(max_length=255)
    skills = models.TextField(blank=True, null=True)
    imageUrl = models.ImageField(blank = True)
    
    def str(self):
        return f"{self.user.username} VolunteerProfile"

# Model for recording food stocks.
class FoodStock(models.Model):
    food_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    storage_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f"{self.food_type} - {self.quantity}"

# Model for food donations.
class FoodDonation(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='food_donations')
    food_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(blank=True, null=True)
    donation_date = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f"Food Donation by {self.donor.username}"

# Model for monetary donations.
class MonetaryDonation(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('bank_card', 'Bank Card'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    )
    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='monetary_donations')
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    donation_date = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f"Monetary Donation by {self.donor.username}"

# Model for food aid requests.
class FoodAidRequest(models.Model):
    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    beneficiary = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='food_aid_requests')
    requested_items = models.TextField()  
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    
    def str(self):
        return f"Food Aid Request by {self.beneficiary.username}"

# Model for planning distribution routes.
class DistributionPlan(models.Model):
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    assigned_volunteers = models.ManyToManyField(VolunteerProfile, blank=True)
    route_details = models.TextField(blank=True, null=True)
    scheduled_date = models.DateTimeField()
    plan_status = models.CharField(max_length=20, default='planned')
    
    def str(self):
        return f"Distribution Plan from {self.start_point} to {self.end_point}"

# Model for managing collection points.
class CollectionPoint(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    def str(self):
        return self.name

# Model for assigning volunteers to tasks or requests.
class VolunteerAssignment(models.Model):
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='assignments')
    food_aid_request = models.ForeignKey(FoodAidRequest, on_delete=models.CASCADE, related_name='assignments', blank=True, null=True)
    assignment_date = models.DateTimeField(auto_now_add=True)
    task_details = models.TextField(blank=True, null=True)
    
    def str(self):
        return f"Assignment for {self.volunteer.user.username}"

# Model for notifications.
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def str(self):
        return f"Notification for {self.user.username}"

# Model for support tickets.
class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def str(self):
        return f"Ticket: {self.subject} by {self.user.username}"
