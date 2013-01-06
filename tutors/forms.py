__author__ = 'Oliver'

from django import forms
from course_manage.models import Course
from tutors.models import Tutor
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def is_email_used(email):
    tutors = Tutor.objects.filter(email=email)
    users = User.objects.filter(email=email)
    if tutors.count() > 0 or users.count() > 0:
        raise ValidationError(u'This email is being used already.')

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
    name = forms.CharField(label=u'Displayed Name')
    email = forms.EmailField(label=u'Student Contact Email')
    phone = forms.CharField(required = False)

    taught_courses = CourseChoiceField(queryset = Course.objects.all(),
                                       widget = forms.SelectMultiple())
    rate = forms.DecimalField(decimal_places = 2, max_digits = 10,
                              widget = forms.TextInput(attrs = {'placeholder': "CAD / Hour"}))
    qualifications = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': u"A few lines about your "
                                                                                     u"education background",
                                                                      'rows': '3'}))

    def __init__(self, tutor, *args, **kwargs):
        self.tutor = tutor
        super(TutorProfileForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != self.tutor.email:
            is_email_used(email)
        return email
