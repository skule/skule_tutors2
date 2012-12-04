from django.db import models
from django.contrib.auth.models import User
from course_manage.models import Course
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.contenttypes.models import ContentType

class Tutor(models.Model):
    # personal info
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    phone = models.CharField(max_length = 20, blank = True)

    # tutor info
    qualifications = models.TextField()
    taught_courses = models.ManyToManyField(Course, null = True)
    rate = models.DecimalField(decimal_places = 2, max_digits = 10)

    # system info
    auth = models.OneToOneField(User, null = True)
    approved = models.BooleanField(default = False)
    last_updated = models.DateTimeField(auto_now = True, auto_created = True)

    def __unicode__(self):
        return self.name

    def qualifications_as_list(self):
        return self.qualifications.split('\n')

        # TODO use python phonenumbers to process the phone number


@receiver(post_delete, sender = Tutor)
def Tutor_delete_handler(sender, instance, **kwargs):
    user = instance.auth
    if not user.is_staff and not user.is_superuser:
        user.delete()

        # add admin log entry for user deletion
        delete_entries = LogEntry.objects.filter(content_type__pk = ContentType.objects.get_for_model(instance).pk,
                                                 object_id = instance.pk, action_flag = DELETION)\
        .order_by('-action_time')
        # add log entry only if tutor is deleted via the admin interface
        if delete_entries:
            delete_entry = delete_entries[ 0 ]
            LogEntry.objects.log_action(
                user_id = delete_entry.user.pk,
                content_type_id = ContentType.objects.get_for_model(user).pk,
                object_id = user.pk,
                object_repr = unicode(user.email),
                action_flag = DELETION,
                change_message = unicode('deleted user per Tutor_delete_handler signal')
            )
