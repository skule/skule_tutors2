from django.db import models
from django.contrib.auth.models import User
from course_manage.models import Course

class Tutor(models.Model):
    # personal info
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    phone = models.CharField(max_length = 20)

    # tutor info
    description = models.TextField()
    taught_courses = models.ManyToManyField(Course, null = True)
    rate = models.DecimalField(decimal_places = 2, max_digits = 10)

    # system info
    auth = models.OneToOneField(User, null = True)
    approved = models.BooleanField(default = False)
    last_updated = models.DateTimeField(auto_now = True, auto_created = True)

    def __unicode__(self):
        return self.name

        # TODO use python phonenumbers to process the phone number
