from django.contrib import admin

from usersettings.models import DRI, Profile
from planning.models import MealSetting

class DRIInline(admin.TabularInline):
    model = DRI
    extra = 1

class MealSettingInline(admin.TabularInline):
    model = MealSetting
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    inlines = (DRIInline, MealSettingInline)

admin.site.register(Profile, ProfileAdmin)
