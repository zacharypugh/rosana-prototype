from rest_framework import serializers
from .models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'account_type', 'fips_codes',
            'company_name', 'mailing_address', 'account_standing', 'subscription_end_date'
        ]