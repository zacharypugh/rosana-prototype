# preferences.py
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)  # frozen=True makes it immutable and safe
class Preference:
    long_name: str = ""
    abbreviation: str = ""
    symbol: str = ""
    conversion_factor: float = 0.0

class LanguagePreferences(Enum):
    # LANGUAGE PREFERENCES
    ENUS = Preference(
    long_name='English (US)',
    abbreviation='EN-US'
    )
    FRCA = Preference(
        long_name='Français (Canada)',
        abbreviation='FR-CA'
    )
    ES419 = Preference(
        long_name='Español (Latinoamericano)',
        abbreviation='ES-419'
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]

class CurrencyPreferences(Enum):
    CAD = Preference(
        long_name = "Canadian Dollar",
        abbreviation="CAD",
        symbol="$"
    )
    EUR = Preference(
        long_name="Euro",
        abbreviation="EUR",
        symbol="€"
    )
    MXN = Preference(
        long_name="México Peso",
        abbreviation="MXN",
        symbol="$"
    )
    USD = Preference(
        long_name="US Dollar",
        abbreviation="USD",
        symbol="$"
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]

class LengthPreferences(Enum):
    METRES = Preference(
        long_name="metres",
        abbreviation="m",
        conversion_factor=1.0
    )
    FEET = Preference(
        long_name="feet",
        abbreviation="ft",
        conversion_factor=3.28084
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]

class DistancePreferences(Enum):
    MILES = Preference(
        long_name="Miles",
        abbreviation="mi",
        conversion_factor=1.0
    )
    KILOMETRES = Preference(
        long_name="Kilometers",
        abbreviation="km",
        conversion_factor=0.621371
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]

class SpeedPreferences(Enum):
    KMPH = Preference(
        long_name="kilometres per hour",
        abbreviation="km/h",
        conversion_factor=1.0
    )
    MPH = Preference(
        long_name="miles per hour",
        abbreviation="mph",
        conversion_factor=0.621371
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]

class AreaSmallPreferences(Enum):
    SQRMETRES = Preference(
        long_name="square metres",
        abbreviation="m²",
        conversion_factor=1.0
    )
    SQRFEET = Preference(
        long_name="square feet",
        abbreviation="ft²",
        conversion_factor=10.7639
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]

class AreaLargePreferences(Enum):
    HECTARES = Preference(
        long_name="hectares",
        abbreviation="ha",
        conversion_factor=1
    )
    ACRES = Preference(
        long_name="acres",
        abbreviation="ac",
        conversion_factor=2.47105
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]

class VolumePreferences(Enum):
    LITRES = Preference(
        long_name="litres",
        abbreviation="L",
        conversion_factor=1.0
    )
    GALLONSUS = Preference(
        long_name="gallons (US)",
        abbreviation="gal (US)",
        conversion_factor=0.264172
    )
    GALLONSIMP = Preference(
        long_name="gallons (Imperial)",
        abbreviation="gal (Imp)",
        conversion_factor=0.219969
    )

    @classmethod
    def choices(cls):
        return [(item.name.lower(), item.value.long_name) for item in cls]