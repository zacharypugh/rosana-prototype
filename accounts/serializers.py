from rest_framework import serializers
from .models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'account_type', 'fips_codes',
            'company_name', 'mailing_address', 'account_standing', 'subscription_end_date'
        ]

class UserSettingsSerializer(serializers.ModelSerializer):
    # Language
    language_display = serializers.CharField(source='language_preference.long_name', read_only=True)
    langauge_abbr = serializers.CharField(source='distance_preference.abbreviation', read_only=True)

    # Currency
    currency_display = serializers.CharField(source='currency_preference.long_name', read_only=True)
    currency_abbr = serializers.CharField(source='currency_preference.abbreviation', read_only=True)
    currency_factor = serializers.FloatField(source='currency_preference.conversion_factor', read_only=True)

    # Length
    length_display = serializers.CharField(source='length_preference.long_name', read_only=True)
    length_abbr = serializers.CharField(source='length_preference.abbreviation', read_only=True)
    length_factor = serializers.FloatField(source='length_preference.conversion_factor', read_only=True)

    # Distance
    distance_display = serializers.CharField(source='distance_preference.long_name', read_only=True)
    distance_abbr = serializers.CharField(source='distance_preference.abbreviation', read_only=True)
    distance_factor = serializers.FloatField(source='distance_preference.conversion_factor', read_only=True)

    # Speed
    speed_display = serializers.CharField(source='speed_preference.long_name', read_only=True)
    speed_abbr = serializers.CharField(source='speed_preference.abbreviation', read_only=True)
    speed_factor = serializers.FloatField(source='speed_preference.conversion_factor', read_only=True)

    # Area small
    area_small_display = serializers.CharField(source='area_small_preference.long_name', read_only=True)
    area_small_abbr = serializers.CharField(source='area_small_preference.abbreviation', read_only=True)
    area_small_factor = serializers.FloatField(source='area_small_preference.conversion_factor', read_only=True)

    # Area large
    area_large_display = serializers.CharField(source='area_large_preference.long_name', read_only=True)
    area_large_abbr = serializers.CharField(source='area_large_preference.abbreviation', read_only=True)
    area_large_factor = serializers.FloatField(source='area_large_preference.conversion_factor', read_only=True)

    # Volume
    volume_display = serializers.CharField(source='area_large_preference.long_name', read_only=True)
    volume_abbr = serializers.CharField(source='area_large_preference.abbreviation', read_only=True)
    volume_factor = serializers.FloatField(source='area_large_preference.conversion_factor', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'distance_unit', 'distance_display', 'distance_abbr', 'distance_factor',
            'area_unit', 'area_display', 'area_abbr', 'area_factor'
        ]