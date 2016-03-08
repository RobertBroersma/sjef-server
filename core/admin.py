from django.contrib import admin

from core.models import Tag, NutritionalValue

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
admin.site.register(NutritionalValue, TagAdmin)
