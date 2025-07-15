from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'uploaded_at')
    search_fields = ('full_name', 'email', 'skills', 'user__username')
    list_filter = ('uploaded_at', 'user')
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at',)
