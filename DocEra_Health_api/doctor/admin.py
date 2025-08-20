from django.contrib import admin
from .models import Doctor, Designation, Specialization, AvailableTime, Review

# Register your models here.
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Doctor)
admin.site.register(Designation, DesignationAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(AvailableTime)
admin.site.register(Review)