from django.contrib import admin
from .models import EnterpriseUserProfile, PersonalUserProfile
# Register your models here.

admin.site.register(EnterpriseUserProfile)
admin.site.register(PersonalUserProfile)
