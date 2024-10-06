from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from activity.models import Workout

class UserProfileInline(admin.StackedInline):
    '''
    Profile object is displayed as part of CustomUser object
    '''
    model = Profile
    can_delete = False #to prevent profile deletion

class WorkoutInline(admin.StackedInline):
    '''
    Profile object is displayed as part of CustomUser object
    '''
    model = Workout
    can_delete = False #to prevent profile deletion

class CustomUserAdmin(UserAdmin):
    #fields to display in the admin user list
    list_display = ('email', 'username', 'is_active', 'is_staff')

    #fields to display when editing a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    inlines = [UserProfileInline, WorkoutInline,]  # Add Profile inline to the User admin

    @admin.action(description='Delete selected users')
    def deleteuser(modeladmin, request, queryset):
        non_superuser=queryset.filter(is_superuser=False)
        non_superuser.delete()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Workout)