from django.db import models

class Tutor(models):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    description = models.TextField()
    rate = models.DecimalField()
    last_updated = models.DateTimeField(auto_now=True, auto_created=True)
