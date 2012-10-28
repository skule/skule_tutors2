__author__ = 'Oliver'

from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'skule_tutors2.views.home', name='home'),
                       # url(r'^skule_tutors2/', include('skule_tutors2.foo.urls')),
                       url(r'^application$', TutorApplication),
                       url(r'^search$', SearchTutors)

)