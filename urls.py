from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views import generic
from tutors.models import Tutor
from django.conf import settings
from emailusernames.forms import EmailAuthenticationForm


admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'skule_tutors2.views.home', name='home'),
                       # url(r'^skule_tutors2/', include('skule_tutors2.foo.urls')),
                       url(r'^$',
                           generic.ListView.as_view(queryset = Tutor.objects.filter(approved = True).order_by('?'),
                                                    context_object_name = 'Tutor_list',
                                                    template_name = "tutor_list.html")),

                       url(r'^tutors/', include('tutors.urls')),


                        #Email as username login
                        url(r'^auth/login$', 'django.contrib.auth.views.login',
                            {'authentication_form': EmailAuthenticationForm }, name='login'),

                        url(r'^auth/logout', 'django.contrib.auth.views.logout', {'next_page': '/'}),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)

#TODO switch to gunicorn
# temp static file fix
if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT}),
    )