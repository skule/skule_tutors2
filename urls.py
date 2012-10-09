from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views import generic
from tutors.models import Tutor
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skule_tutors2.views.home', name='home'),
    # url(r'^skule_tutors2/', include('skule_tutors2.foo.urls')),
    url(r'^$', generic.ListView.as_view(queryset=Tutor.objects.all().order_by("name"),
                                        context_object_name='Tutor_list',
                                        template_name="base_list.html")),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
