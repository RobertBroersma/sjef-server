from django.contrib import admin

from planning.models import DayPlanning, WeekPlanning, MealSetting, Meal

class DayPlanningInline(admin.TabularInline):
    model = DayPlanning
    extra = 0

class DayPlanningAdmin(admin.ModelAdmin):
    pass

class WeekPlanningAdmin(admin.ModelAdmin):
    inlines = (DayPlanningInline,)

class MealSettingAdmin(admin.ModelAdmin):
    pass

class MealAdmin(admin.ModelAdmin):
    pass

admin.site.register(DayPlanning, DayPlanningAdmin)
admin.site.register(WeekPlanning, WeekPlanningAdmin)
admin.site.register(MealSetting, MealSettingAdmin)
admin.site.register(Meal, MealAdmin)
