from django.contrib import admin
from models import Course

__author__ = 'Oliver'

class CourseAdmin(admin.ModelAdmin):
    list_display = [ 'year', 'course_code', 'name' ]
    list_filter = [ 'year' ]
    search_fields = [ 'year', 'course_code', 'name' ]

admin.site.register(Course, CourseAdmin)
