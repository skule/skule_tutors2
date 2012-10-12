from django.db import models

class Tutor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    description = models.TextField()
    rate = models.DecimalField(decimal_places=2, max_digits=10)
    approved = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True, auto_created=True)

    def __unicode__(self):
        return self.name

    # TODO use python phonenumbers to process the phone number
