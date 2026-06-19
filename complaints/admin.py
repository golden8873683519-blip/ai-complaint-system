from django.contrib import admin
from django.contrib.auth.models import User

from .models import (
    Complaint,
    UserProfile,
    Department,
    Notification
)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        'complaint_id',
        'title',
        'get_department',
        'status',
        'assigned_to',
        'created_at'
    )

    list_filter = (
        'status',
        'department'
    )

    search_fields = (
        'complaint_id',
        'title',
        'first_name',
        'last_name'

    )

    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs
    ):

        if db_field.name == "assigned_to":

            kwargs["queryset"] = User.objects.filter(
                userprofile__is_department_head=True
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )

    def get_department(self, obj):
        return obj.department.name if obj.department else "-"

    get_department.short_description = "Department"


admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(Notification)
