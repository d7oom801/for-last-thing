from django.contrib import admin
from .models import (CustomUser, Clinic, Patient,
                     Specialization, Doctor, Available,
                     Appointment, Feedback, AuditLog)

admin.site.register(CustomUser)
admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Available)
admin.site.register(Feedback)
admin.site.register(Appointment)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('action', 'ip_address')
    readonly_fields = ('user', 'action', 'ip_address', 'timestamp')