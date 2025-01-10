from django.contrib import admin
from .models import Cat, AdoptionProfile, AdoptionRequest, ModifiedUser

# register models
admin.site.register(Cat)
admin.site.register(AdoptionProfile)
admin.site.register(AdoptionRequest)
admin.site.register(ModifiedUser)