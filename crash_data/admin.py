from django.contrib import admin
from .models import LocalityReference, LocalityPopulation, CrashCase

@admin.register(LocalityReference)
class LocalityReferenceAdmin(admin.ModelAdmin):
    list_display = ('jcode', 'place_name_short', 'county', 'st_name')
    search_fields = ('jcode', 'place_name_short', 'county', 'st_name')

@admin.register(LocalityPopulation)
class LocalityPopulationAdmin(admin.ModelAdmin):
    # Update list_display to only reference existing fields or admin methods
    list_display = ('locality_id', 'get_pop_2020', 'get_pop_2025')

    # Custom methods to safely extract index values for display in the admin table
    @admin.display(description='2020 Pop Estimate')
    def get_pop_2020(self, obj):
        if obj.population_estimates and len(obj.population_estimates) > 20:
            return f"{obj.population_estimates[20]:,}" # Adds comma formatting (e.g. 1,250)
        return "N/A"

    @admin.display(description='2025 Pop Estimate')
    def get_pop_2025(self, obj):
        if obj.population_estimates and len(obj.population_estimates) > 25:
            return f"{obj.population_estimates[25]:,}"
        return "N/A"

@admin.register(CrashCase)
class CrashCaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'locality', 'crash_date', 'severity')
    # Points 'locality__' lookups to your new jcode key structure
    search_fields = ('case_number', 'locality__jcode', 'locality__place_name_short')
    list_filter = ('severity', 'crash_date')