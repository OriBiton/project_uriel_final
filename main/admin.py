from django.contrib import admin

from .models import AvailableMeeting

@admin.register(AvailableMeeting)
class AvailableMeetingAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'is_booked')
