from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from imagekit.processors import ResizeToFill

from django.contrib.auth import get_user_model

import re


# these are choices defined globally to be used by the cat and adoption profile model
age_choices = [
    ('Kitten', 'Kitten'),
    ('Young Adult','Young Adult'),
    ('Adult', 'Adult'),
    ('Senior', 'Senior')
]
sex_choices = [
    ('Male', 'Male'),
    ('Female', 'Female')
]
breed_choices = [
    ('Domestic Shorthair', 'Domestic Shorthair'),
    ('Domestic Longhair','Domestic Longhair'),
    ('Siamese', 'Siamese'),
    ('Ragdoll', 'Ragdoll'),
    ('Tabby', 'Tabby'),
    ('Calico', 'Calico'),
    ('Tortoiseshell', 'Tortoiseshell'),
    ('Russian Blue', 'Russian Blue'),
    ('Tuxedo', 'Tuxedo'),
    ('Persian', 'Persian'),
    ('Bombay', 'Bombay'),
    ('Maine Coon', 'Maine Coon'),
    ('Sphynx', 'Sphynx')
]
coat_choices = [
    ('Short', 'Short'),
    ('Medium', 'Medium'),
    ('Long', 'Long'),
]
temperament_choices = [
    ('Shy', 'Shy'),
    ('Calm', 'Calm'),
    ('Social', 'Social'),
    ('Playful', 'Playful'),
]

# these are all the street types in Canada according to Canada Post (I didn't want to put it in the
# class because of how many lines it is)
street_types = [
'ABBEY', 'ACRES', 'ALLEY', 'AVENUE', 'BAY',
    'BEACH', 'BEND', 'BOULEVARD', 'BYPASS', 'BYWAY',
    'CAMPUS', 'CAPE', 'CENTRE', 'CHASE', 'CIRCLE',
    'CIRCUIT', 'CLOSE', 'COMMON', 'CONCESSION', 'CORNERS',
    'COURT', 'COVE', 'CRESCENT', 'CROSSING', 'CUL-DE-SAC',
    'DALE', 'DELL', 'DIVERSION', 'DOWNS', 'DRIVE',
    'END', 'ESPLANADE', 'ESTATES', 'EXPRESSWAY', 'EXTENSION',
    'FARM', 'FIELD', 'FOREST', 'FREEWAY', 'FRONT',
    'GARDENS', 'GATE', 'GLADE', 'GLEN', 'GREEN',
    'GROUNDS', 'GROVE', 'HARBOUR', 'HEATH', 'HEIGHTS',
    'HIGHLANDS', 'HIGHWAY', 'HILL', 'HOLLOW', 'INLET',
    'ISLAND', 'KEY', 'KNOLL', 'LANDING', 'LANE',
    'LIMITS', 'LINE', 'LINK', 'LOOKOUT', 'LOOP',
    'MALL', 'MANOR', 'MAZE', 'MEADOW', 'MEWS',
    'MOOR', 'MOUNT', 'MOUNTAIN', 'ORCHARD', 'PARADE',
    'PARK', 'PARKWAY', 'PASSAGE', 'PATH', 'PATHWAY',
    'PINES', 'PLACE', 'PLATEAU', 'PLAZA', 'POINT',
    'PORT', 'PRIVATE', 'PROMENADE', 'QUAY', 'RAMP',
    'RANGE', 'RIDGE', 'RISE', 'ROAD', 'ROUTE',
    'ROW', 'RUN', 'SQUARE', 'STREET', 'SUBDIVISION',
    'TERRACE', 'THICKET', 'TOWERS', 'TOWNLINE', 'TRAIL',
    'TURNABOUT', 'VALE', 'VIA', 'VILLAGE', 'VILLAS',
    'VISTA', 'WALK', 'WAY', 'WHARF', 'WOOD', 'WYND'
]

# extend the existing Django user model to include a profile picture
class ModifiedUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to='profile/',
        processors=[ResizeToFill(50,50)],
        format='JPEG',
        options={'quality': 100},
        null=False,
        blank=False)

User = get_user_model() # user needs to be defined like this because of the custom user model

class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100, choices=age_choices, verbose_name='Age')
    photo = ProcessedImageField(
        upload_to='cats/',
        processors=[ResizeToFit(400)],
        format='JPEG',
        options={'quality': 70})
    sex = models.CharField(max_length=6, choices=sex_choices, verbose_name='Sex')
    breed = models.CharField(max_length=100, choices=breed_choices, verbose_name='Breed')
    coat_length = models.CharField(max_length=10, choices=coat_choices, verbose_name='Coat length')
    temperament = models.CharField(max_length=20, choices=temperament_choices, verbose_name='Temperament')
    has_special_needs = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# street type validator
def validate_street_type(value):
    street_type = value
    # convert to uppercase to align with how the choices in the array are written
    street_type = street_type.upper()
    # if the input doesn't match any of the valid street types, throw error
    if not any(street_type == valid_street_type for valid_street_type in street_types):
        # I have chosen not to accept abbreviations because they are too inconsistent
        # a court street type could be abbreviated to crt or ct, etc
        raise ValidationError('Street must have a valid non-abbreviated street type (eg. ROAD not RD)')


# phone number validator (same as the function from assignment 2 but modified for python)
def validate_phone(value):
    phone = value
    if re.search(r'[A-Za-z]', phone): # check for alphabetical characters
        raise ValidationError('Invalid phone number.')
    if phone[0] == '+': # check if the number has a non canadian country code
        if len(phone) >= 2 and phone[1] not in ('0', '1'):
            raise ValidationError('Invalid phone number.')
        phone = phone[2:] # if the country code is valid, trim it from the phone number and continue
    phone = re.sub(r'[^0-9]', '', phone) # remove any further non-numerical characters
    if len(phone) != 10: # a valid phone number should have 10 digits at this point
        raise ValidationError('Invalid phone number.')

class AdoptionProfile(models.Model):
    province_choices = [
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('MB', 'Manitoba'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NT', 'Northwest Territories'),
        ('NS', 'Nova Scotia'),
        ('NU', 'Nunavut'),
        ('ON', 'Ontario'),
        ('PE', 'Prince Edward Island'),
        ('QC', 'Quebec'),
        ('SK', 'Saskatchewan'),
        ('YT', 'Yukon')
    ]

    # this uses the existing choices for various fields from the cat model, just adding
    # on the "no preference" option
    age_choices.append (('no_preference', 'No Preference'))
    sex_choices.append (('no_preference', 'No Preference'))
    breed_choices.append (('no_preference', 'No Preference'))
    coat_choices.append (('no_preference', 'No Preference'))
    temperament_choices.append (('no_preference', 'No Preference'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adoption_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20, validators=[validate_phone])

    street_number = models.PositiveIntegerField()
    street_name = models.CharField(max_length=100)
    street_type = models.CharField(max_length=100,validators=[validate_street_type])

    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100, choices=province_choices)

    has_children = models.BooleanField(default=False)
    has_pets = models.BooleanField(default=False)
    has_allergies = models.BooleanField(default=False)

    # these are preferences that align with the cat fields, they were intended to automatically
    # filter the cats page based on the saved preferences from the user but I was not able to accomplish
    # this functionality
    sex = models.CharField(max_length=15, choices=sex_choices, default = 'no_preference')
    age = models.CharField(max_length=100, choices=age_choices, default = 'no_preference')
    breed = models.CharField(max_length=100, choices=breed_choices, default = 'no_preference')
    coat_length = models.CharField(max_length=15, choices=coat_choices, default = 'no_preference')
    temperament = models.CharField(max_length=20, choices=temperament_choices, default = 'no_preference')
    special_needs_pref = models.BooleanField(default=False)
    several_cats_pref = models.BooleanField(default=False)

class AdoptionRequest(models.Model):
    status_choices = [
        ('Pending', 'Pending'),
        ('Decision Made', 'Decision made')
    ]
    # the status of an adoption request is set to pending upon creation and would be marked decision made
    # by a hypothetical admin
    status = models.CharField(max_length=100, choices=status_choices, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'adoption_request')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='adoption_request')
    date = models.DateField()