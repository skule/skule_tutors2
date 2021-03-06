from django.db import models

# Create your models here.

class Course(models.Model):
    year = models.SmallIntegerField(verbose_name = 'Course Year')
    course_code = models.CharField(verbose_name = 'Course Code', max_length = 7, primary_key = True)
    name = models.CharField(verbose_name = 'Course Name', max_length = 50)

    description = models.TextField(blank = True)

    def save(self, *args, **kwargs):
        """ Make the course code always in upper case """
        self.course_code = str(self.course_code).upper()
        super(Course, self).save()

    def option_label(self):
        return self.course_code + ' | ' + self.name

    def __unicode__(self):
        return self.course_code

        #    def get_absolute_url(self):
        #        """
        #        returns the url of this course.
        #        """
        #        return reverse('engsci_conga.views.courses_view', kwargs = {'course': self.course_code})