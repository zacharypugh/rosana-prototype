from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('admin', 'Admin'),
    ]
    
    # New configuration options for account standing states
    STANDING_CHOICES = [
        ('good', 'Good Standing'),
        ('suspended', 'Suspended'),
        ('blocked', 'Blocked'),
    ]
    
    account_type = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='regular'
    )
    
    fips_codes = ArrayField(
        models.CharField(max_length=7), 
        default=list, 
        blank=True
    )

    company_name = models.CharField(
        max_length=150, 
        blank=True, 
        null=True
    )
    
    mailing_address = models.TextField(
        blank=True, 
        null=True
    )
    
    account_standing = models.CharField(
        max_length=15,
        choices=STANDING_CHOICES,
        default='good'
    )
    
    subscription_end_date = models.DateField(
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.username