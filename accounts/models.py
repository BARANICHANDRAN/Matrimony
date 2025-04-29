from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        if not self.email:
            raise ValueError("Email is required")
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15,null=True, blank=True,unique=True)
    dob = models.DateField(null=True, blank=True)  
    age = models.PositiveIntegerField(editable=False) 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    location = models.CharField(max_length=255)
    bio = models.TextField(blank=False)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.dob:
            today = date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email
