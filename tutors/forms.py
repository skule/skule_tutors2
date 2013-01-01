__author__ = 'Oliver'

from django import forms
from course_manage.models import Course

class CourseChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        try:
            return obj.course_code + ": " + obj.name
        except AttributeError:
            return unicode(obj)

class ApplicationForm(forms.Form):
    """
    Form for tutor applications
    """

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField(required = False)

    # TODO use chosen for the multi-select field http://harvesthq.github.com/chosen/
    # or http://ivaynberg.github.com/select2/
    taught_courses = CourseChoiceField(queryset = Course.objects.all(),
                                       widget = forms.SelectMultiple())
    rate = forms.DecimalField(decimal_places = 2, max_digits = 10,
                              widget = forms.TextInput(attrs = {'placeholder': "CAD / Hour"}))
    qualifications = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': "A few lines about your education "
                                                                                     "background",
                                                                      'rows': '3'}))


class TutorProfileForm(forms.Form):
    """
    Form for tutor profile editing
    """
    name = forms.CharField(label='Displayed Name')
    email = forms.EmailField(label='Student Contact Email')
    phone = forms.CharField(required = False)

    taught_courses = CourseChoiceField(queryset = Course.objects.all(),
                                       widget = forms.SelectMultiple())
    rate = forms.DecimalField(decimal_places = 2, max_digits = 10,
                              widget = forms.TextInput(attrs = {'placeholder': "CAD / Hour"}))
    qualifications = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': "A few lines about your education "
                                                                                     "background",
                                                                      'rows': '3'}))
