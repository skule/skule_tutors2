from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from course_manage.models import Course
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.contenttypes.models import ContentType
from django.http import QueryDict

def validate_rate_positive(value):
    if value < 0:
        raise ValidationError(u"%s is not a valid rate" % value)

class Tutor(models.Model):
    # personal info
    name = models.CharField(max_length = 50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 20, blank = True)

    # tutor info
    qualifications = models.TextField(blank=True)
    taught_courses = models.ManyToManyField(Course, null = True)
    rate = models.DecimalField(decimal_places = 2, max_digits = 10, default=0, validators=[validate_rate_positive])

    # system info
    auth = models.OneToOneField(User, null = True, editable=False)
    approved = models.BooleanField(default = False)
    last_updated = models.DateTimeField(auto_now = True, auto_created = True, editable=False)

    def __unicode__(self):
        return self.name

    def displayed_rate(self):
        if self.rate > 0:
            return unicode(self.rate)
        else:
            return 'Rate provided upon request'

    def qualifications_as_list(self):
        return self.qualifications.split('\n')

    def POST_data(self):
        """
        Returns the personal info and the tutor info of this profile as
        if it was a queryDict from a post request
        """
        data = QueryDict('').copy()
        data.update({'name':self.name,
                     'email':self.email,
                     'phone':self.phone,
                     'qualifications':self.qualifications,
                     'rate':str(self.rate)})
        for course in self.taught_courses.all():
            data.update({'taught_courses':course.course_code})
        return data


        # TODO use python phonenumbers to process the phone number


@receiver(post_delete, sender = Tutor)
def Tutor_delete_handler(sender, instance, **kwargs):
    user = instance.auth
    if not user.is_staff and not user.is_superuser: # OMG I used DeMorgan's theorem
        user.delete()

        # add admin log entry for user deletion
        delete_entries = LogEntry.objects.filter(content_type__pk = ContentType.objects.get_for_model(instance).pk,
                                                 object_id = instance.pk, action_flag = DELETION)\
        .order_by('-action_time')
        # add log entry only if tutor is deleted via the admin interface
        if delete_entries:
            # TODO create entry only if deleted in the last 30 secs
            delete_entry = delete_entries[ 0 ]
            LogEntry.objects.log_action(
                user_id = delete_entry.user.pk,
                content_type_id = ContentType.objects.get_for_model(user).pk,
                object_id = user.pk,
                object_repr = unicode(user.email),
                action_flag = DELETION,
                change_message = unicode('deleted user per Tutor_delete_handler signal')
            )

@receiver(post_save, sender = User)
def Create_tutor_from_user(sender, instance, **kwargs):
    try:
        Tutor.objects.get(auth = instance)
    except ObjectDoesNotExist:
        tutor = Tutor.objects.create(name = instance.get_full_name(),
                                     email = instance.email,
                                     rate = 0,
                                     auth = instance)
        tutor.save(force_update=True)