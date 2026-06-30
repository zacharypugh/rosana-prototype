from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from .preferences import LanguagePreferences, CurrencyPreferences, LengthPreferences, DistancePreferences, SpeedPreferences, AreaSmallPreferences, AreaLargePreferences, VolumePreferences

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

    language_preference = models.CharField(
        max_length=20,
        choices=LanguagePreferences.choices(),
        default=LanguagePreferences.ENUS
    )

    currency_preference = models.CharField(
        max_length=20,
        choices=CurrencyPreferences.choices(),
        default=CurrencyPreferences.USD
    )

    length_preference = models.CharField(
        max_length=20,
        choices=LengthPreferences.choices(),
        default=LengthPreferences.FEET
    )

    distance_preference = models.CharField(
        max_length=20,
        choices=DistancePreferences.choices(),
        default=DistancePreferences.MILES
    )

    speed_preference = models.CharField(
        max_length=20,
        choices=SpeedPreferences.choices(),
        default=SpeedPreferences.MPH
    )

    area_small_preference = models.CharField(
        max_length=20,
        choices=AreaSmallPreferences.choices(),
        default=AreaSmallPreferences.SQRFEET
    )

    area_large_preference = models.CharField(
        max_length=20,
        choices=AreaLargePreferences.choices(),
        default=AreaLargePreferences.ACRES
    )

    volume_preference = models.CharField(
        max_length=20,
        choices=VolumePreferences.choices(),
        default=VolumePreferences.GALLONSUS
    )

    @property
    def get_language_preference(self):
        try:
            return LanguagePreferences[self.language_preference].value
        except KeyError:
            return LanguagePreferences.ENUS.value
        
    @property
    def get_currency_preference(self):
        try:
            return CurrencyPreferences[self.currency_preference].value
        except KeyError:
            return CurrencyPreferences.USD.value
        
    @property
    def get_length_preference(self):
        try:
            return LengthPreferences[self.length_preference].value
        except KeyError:
            return LengthPreferences.FEET.value

    @property
    def get_distance_preference(self):
        try:
            return DistancePreferences[self.distance_preference].value
        except KeyError:
            return DistancePreferences.MILES.value
        
    @property
    def get_speed_preference(self):
        try:
            return SpeedPreferences[self.speed_preference].value
        except KeyError:
            return SpeedPreferences.MPH.value
        
    @property
    def get_area_small_preference(self):
        try:
            return AreaSmallPreferences[self.area_small_preference].value
        except KeyError:
            return AreaSmallPreferences.SQRFEET.value
        
    @property
    def get_area_large_preference(self):
        try:
            return AreaLargePreferences[self.area_large_preference].value
        except KeyError:
            return AreaLargePreferences.ACRES.value
        
    @property
    def get_volume_preference(self):
        try:
            return VolumePreferences[self.volume_preference].value
        except KeyError:
            return VolumePreferences.GALLONSUS.value

    def __str__(self):
        return self.username