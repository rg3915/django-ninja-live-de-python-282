from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_completed', 'user__first_name', 'user__last_name')
    search_fields = ('title',)
