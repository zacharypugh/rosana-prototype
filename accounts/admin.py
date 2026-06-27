from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Info', {'fields': (
            'account_type', 
            'fips_codes', 
            'company_name', 
            'mailing_address', 
            'account_standing', 
            'subscription_end_date'
        )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Profile Info', {'fields': (
            'account_type', 
            'fips_codes', 
            'company_name', 
            'mailing_address', 
            'account_standing', 
            'subscription_end_date'
        )}),
    )

admin.site.register(CustomUser, CustomUserAdmin)