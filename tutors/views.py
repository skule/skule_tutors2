from emailusernames.forms import EmailUserCreationForm
from django.contrib.auth.models import Group
from forms import ApplicationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from emailusernames.utils import create_user
from models import Tutor
# Create your views here.

def TutorApplication(request, template = 'tutors/tutor_application.html'):
    if request.method == 'POST':
        user_creation_form = EmailUserCreationForm(request.POST)
        profile_creation_form = ApplicationForm(request.POST)

        if user_creation_form.is_valid() and profile_creation_form.is_valid():
            # Create the user
            user_data = user_creation_form.cleaned_data
            user = create_user(user_data[ 'email' ], user_data[ 'password1' ])

            tutors_group = Group.objects.filter(name = 'Tutors')
            if not tutors_group:
                Group(name = 'Tutors').save()

            user.is_staff = False
            user.groups.add(tutors_group[ 0 ])

            profile_data = profile_creation_form.cleaned_data
            user.first_name = profile_data[ 'first_name' ]
            user.last_name = profile_data[ 'last_name' ]
            user.save()

            # Create the tutor profile
            tutor = Tutor(
                name = profile_data[ 'first_name' ] + ' ' + profile_data[ 'last_name' ],
                email = user_data[ 'email' ],
                phone = profile_data[ 'phone' ],
                description = profile_data[ 'description' ],
                rate = profile_data[ 'rate' ],
                auth = user,
            )
            tutor.save()
            for course in profile_data[ 'taught_courses' ]:
                tutor.taught_courses.add(course)
            tutor.save()

            return HttpResponseRedirect('/')
    else:
        user_creation_form = EmailUserCreationForm()
        profile_creation_form = ApplicationForm()

    return render_to_response(template,
                              dict(user_creation_form = user_creation_form,
                                   profile_creation_form = profile_creation_form),
                              context_instance = RequestContext(request))

