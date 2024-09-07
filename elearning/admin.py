from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class StatusUpdatesAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'date_added')

admin.site.register(StatusUpdates, StatusUpdatesAdmin)

class CoursesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description', 'length_in_weeks', 'semester', 'date_added')
    ordering = ['date_added']

admin.site.register(Courses, CoursesAdmin)

class CourseLinkInLine(admin.TabularInline):
    model = Courses
    extra = 0

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('startMonth', 'startYear')
    inlines = [CourseLinkInLine]

    ordering = ['startYear']

admin.site.register(Semester, SemesterAdmin)

class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'type', 'title', 'description', 'week', 'date_added', 'file')

admin.site.register(CourseMaterial, CourseMaterialAdmin)

class CourseDueDatesAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'type', 'title', 'description', 'date_added', 'date_due')

admin.site.register(CourseDueDates, CourseDueDatesAdmin)

class RegistrationsAdmin(admin.ModelAdmin):
    list_display = ('status', 'student', 'course', 'note', 'registration_date')

admin.site.register(Registrations, RegistrationsAdmin)

class CourseFeedbackAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'rating', 'feedback', 'student_id', 'date_posted')

admin.site.register(CourseFeedback, CourseFeedbackAdmin)

class ChatMessagesAdmin(admin.ModelAdmin):
    list_display = ('text', 'room', 'timestamp')

admin.site.register(ChatMessages, ChatMessagesAdmin)

admin.site.register(AppUser)
