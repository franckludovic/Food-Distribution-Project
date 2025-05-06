from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
import datetime
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, default=0)
    USER_TYPE_CHOICES = (
        ('manager', 'Manager'),
        ('volunteer', 'Volunteer'),
        ('beneficiary', 'Beneficiary'),
        ('donor', 'Donor'),
    )
    phone = models.CharField(max_length=35, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='beneficiary')
    groups = models.ManyToManyField(Group, related_name="profile_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="profile_permissions", blank=True)
    id_user = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username

class Food(models.Model):
    FOOD_TYPE_CHOICES = (
        ('grains', 'Grains'),
        ('canned', 'Canned'),
        ('dried', 'Dried'),
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('frozen', 'Frozen'),
        ('baked', 'Baked'),
        ('dairy', 'Dairy'),
        ('meat', 'Meat'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('spices', 'Spices'),
    )
    food_id = models.AutoField(primary_key=True)
    food_name = models.TextField(blank=True)
    food_type = models.CharField(max_length=50, choices=FOOD_TYPE_CHOICES, default='')
    created_at = models.DateField(default=datetime.date.today)
    expire_date = models.DateField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False)
    storage_location = models.TextField(blank=True)

    def __str__(self):
        return self.food_name

class BeneficiaryProfile(models.Model):
    REGION_CHOICES = (
        ('adamawa', 'Adamawa'),
        ('centre', 'Centre'),
        ('east', 'East'),
        ('far_north', 'Far North'),
        ('littoral', 'Littoral'),
        ('north', 'North'),
        ('south', 'South'),
        ('south_west', 'South-West'),
        ('west', 'West'),
        ('north_west', 'North-West'),
    )

    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='beneficiary_profile')
    number_of_dependents = models.IntegerField(default=0)
    specific_needs = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255) 
    region = models.CharField(max_length=50, choices=REGION_CHOICES, default='littoral')  

    def __str__(self):
        return f"{self.user.user.username} BeneficiaryProfile"

class VolunteerProfile(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    availability = models.TextField() 
    intervention_area = models.CharField(max_length=255)
    skills = models.TextField(blank=True, null=True)
    imageUrl = models.ImageField(upload_to="volunteer_images/", blank=True, null=True)
    isAvailable = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.user.username} VolunteerProfile"

class FoodStock(models.Model):
    FOOD_TYPE_CHOICES = (
        ('grains', 'Grains'),
        ('canned', 'Canned'),
        ('dried', 'Dried'),
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('frozen', 'Frozen'),
        ('baked', 'Baked'),
        ('dairy', 'Dairy'),
        ('meat', 'Meat'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('spices', 'Spices'),
    )
    food_type = models.CharField(max_length=100, choices=FOOD_TYPE_CHOICES, default='')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.food_type} - {self.quantity}"

class FoodDonation(models.Model):
    donor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='food_donations')
    food_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(blank=True, null=True)
    donation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Food Donation by {self.donor.user.username}"

class MonetaryDonation(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('bank_card', 'Bank Card'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    )
    MonetaryDonation_id = models.AutoField(primary_key=True, default=1)
    donor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='monetary_donations')
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    donation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Monetary Donation by {self.donor.user.username}"

class FoodAidRequest(models.Model):
    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    beneficiary = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='food_aid_requests')
    requested_items = models.TextField()  
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    
    def __str__(self):
        return f"Food Aid Request by {self.beneficiary.user.username}"

class DistributionPlan(models.Model):
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    assigned_volunteers = models.ManyToManyField(VolunteerProfile, blank=True)
    route_details = models.TextField(blank=True, null=True)
    scheduled_date = models.DateTimeField()
    plan_status = models.CharField(max_length=20, default='planned')
    
    def __str__(self):
        return f"Distribution Plan from {self.start_point} to {self.end_point}"

class CollectionPoint(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    def __str__(self):
        return self.name

class VolunteerAssignment(models.Model):
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='assignments')
    food_aid_request = models.ForeignKey(FoodAidRequest, on_delete=models.CASCADE, related_name='assignments', blank=True, null=True)
    assignment_date = models.DateTimeField(auto_now_add=True)
    task_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Assignment for {self.volunteer.user.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user.user.username}"

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Ticket: {self.subject} by {self.user.user.username}"
