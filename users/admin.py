# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MenteeProfile, CaseManagerProfile, Mentee, CaseManager

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'type', 'is_verified', 'is_staff', 'date_joined')
    list_filter = ('type', 'is_verified', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'gender', 'profile_picture', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('User Type', {'fields': ('type', 'is_verified')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'type', 'is_verified', 'is_staff'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)

# Inline classes for profiles
class MenteeProfileInline(admin.StackedInline):
    model = MenteeProfile
    can_delete = False
    verbose_name_plural = 'Mentee Profile'
    fk_name = 'user'  # Specify which ForeignKey links to Mentee (User)

class CaseManagerProfileInline(admin.StackedInline):
    model = CaseManagerProfile
    can_delete = False
    verbose_name_plural = 'Case Manager Profile'
    fk_name = 'user'  # Specify which ForeignKey links to CaseManager (User)

class MenteeAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'get_case_manager')
    list_filter = ('is_verified',)
    search_fields = ('email', 'first_name', 'last_name')
    inlines = [MenteeProfileInline]

    def get_case_manager(self, obj):
        return obj.profile.case_manager.email if obj.profile and obj.profile.case_manager else 'None'
    get_case_manager.short_description = 'Case Manager'

class CaseManagerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'get_mentee_count')
    list_filter = ('is_verified',)
    search_fields = ('email', 'first_name', 'last_name')
    inlines = [CaseManagerProfileInline]

    def get_mentee_count(self, obj):
        return obj.get_mentee_count() if obj.profile else 0
    get_mentee_count.short_description = 'Mentee Count'

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Mentee, MenteeAdmin)
admin.site.register(CaseManager, CaseManagerAdmin)