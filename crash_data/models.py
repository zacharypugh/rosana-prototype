from django.db import models
from django.contrib.postgres.fields import ArrayField # 👈 Import PostgreSQL specific ArrayField

class LocalityReference(models.Model):
    # Derived from CensusPlaceCode
    jcode = models.CharField(max_length=50, unique=True, primary_key=True)
    
    # Text-based location descriptors
    st = models.CharField(max_length=10, default="")                # e.g., "IA"
    st_name = models.CharField(max_length=100, default="")          # e.g., "Iowa"
    county = models.CharField(max_length=150, default="")           # e.g., "Adair"
    place_name_long = models.CharField(max_length=250, default="")   # e.g., "City Of Adair..."
    place_name_short = models.CharField(max_length=250, default="")  # e.g., "Adair [Adair Co]"
    census_place_name = models.CharField(max_length=250, default="") # e.g., "Adair City (Pt.)"

    def __str__(self):
        return f"{self.jcode} - {self.place_name_short}, {self.st}"

    class Meta:
        verbose_name = "Locality Reference"
        verbose_name_plural = "Locality References"

class LocalityPopulation(models.Model):
    # Assuming locality is a ForeignKey or OneToOneField linking to LocalityReference
    locality = models.OneToOneField(
        'LocalityReference', 
        on_delete=models.CASCADE, 
        primary_key=True,
        to_field='jcode'
    )
    
    # Store the population list as an integer array field
    # We also define a default empty list factory to prevent database errors
    population_estimates = ArrayField(
        models.IntegerField(),
        default=list,
        help_text="Array of population estimates where index 0 = Year 2000, index 20 = Year 2020, etc."
    )

    def __str__(self):
        return f"Population matrix for {self.locality_id}"

class CrashCase(models.Model):
    # Update your foreign key link to point directly to the localized level
    locality = models.ForeignKey(
        LocalityReference, 
        on_delete=models.CASCADE, 
        related_name='crashes'
    )
    case_number = models.CharField(max_length=50, unique=True)
    crash_date = models.DateField()
    severity = models.CharField(max_length=20, default='minor')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Case {self.case_number} - Locality {self.locality_id}"