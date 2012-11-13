__author__ = 'Oliver'

from django import forms
from course_manage.models import Course

class ApplicationForm(forms.Form):
    """
    Form for tutor applications
    """

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField(required = False)

    # TODO use chosen for the multi-select field http://harvesthq.github.com/chosen/
    # or http://ivaynberg.github.com/select2/
    taught_courses = forms.ModelMultipleChoiceField(queryset = Course.objects.all())
    rate = forms.DecimalField(decimal_places = 2, max_digits = 10)
    qualifications = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "A few lines about your education background"}))

    
