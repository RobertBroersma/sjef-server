from django.contrib import admin

from usersettings.models import DRI, Profile

class DRIInline(admin.TabularInline):
    model = DRI
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    inlines = (DRIInline,)

admin.site.register(Profile, ProfileAdmin)
