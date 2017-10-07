from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Person)
admin.site.register(models.Household)
admin.site.register(models.HouseholdStatus)

class IncidentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(models.Incident, IncidentAdmin)