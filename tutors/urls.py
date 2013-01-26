__author__ = 'Oliver'

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('tutors.views',
                       url(r'^application$', 'TutorApplication'),
                       url(r'^search$', 'SearchTutors'),
                       url(r'^profile$', 'TutorProfileEdit')
)