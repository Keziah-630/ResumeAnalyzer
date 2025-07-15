from django.contrib import admin
from .models import Job, JobApplication

admin.site.site_header = "SmartHiring Admin"
admin.site.site_title = "SmartHiring Portal"
admin.site.index_title = "Welcome to SmartHiring Administration"

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'experience_level', 'created_at', 'is_active')
    list_filter = ('job_type', 'experience_level', 'location', 'company', 'is_active')
    search_fields = ('title', 'company', 'location', 'description', 'requirements', 'skills_required')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected jobs as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected jobs as inactive"

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'resume', 'applied_at', 'status')
    list_filter = ('status', 'applied_at', 'job', 'user')
    search_fields = ('job__title', 'user__username', 'resume__full_name')
    ordering = ('-applied_at',)
