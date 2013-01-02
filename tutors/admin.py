__author__ = 'Oliver'

from models import *
from django.contrib import admin

class TutorAdmin(admin.ModelAdmin):
    # list options
    list_display = [ 'name', 'email', 'rate', 'approved' ]
    list_editable = [ 'approved' ]
    list_filter = [ 'rate', 'last_updated', 'approved' ]

    actions = [ 'approveTutor', 'disapproveTutor' ]
    search_fields = [ 'name', 'email', 'phone', 'taught_courses__course_code' ]

    # Model form options
    readonly_fields = [ 'last_updated', 'auth' ]
    filter_horizontal = [ 'taught_courses' ]

    def queryset(self, request):
        '''
        Don't display the staff associated Tutor profiles to non-superusers, ensure no staff accounts can be
        accidentally approved for display.
        '''
        qs = super(TutorAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(auth__is_staff = False)

    def approveTutor(self, request, queryset):
        rows_updated = queryset.update(approved = True)
        if rows_updated == 1:
            message_bit = "1 tutor was" # so much work to be grammatically correct
        else:
            message_bit = "%s tutors were" % rows_updated
        self.message_user(request, "%s successfully approved." % message_bit)
        # TODO add notification to tutor of his profile's status
    approveTutor.short_description = "Approve Selected Tutors"

    def disapproveTutor(self, request, queryset):
        rows_updated = queryset.update(approved = False)
        if rows_updated == 1:
            message_bit = "1 tutor was"
        else:
            message_bit = "%s tutors were" % rows_updated
        self.message_user(request, "%s successfully disapproved." % message_bit)
    disapproveTutor.short_description = "Disapprove Selected Tutors"

admin.site.register(Tutor, TutorAdmin)