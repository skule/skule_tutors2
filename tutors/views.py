from emailusernames.forms import EmailUserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from forms import ApplicationForm, TutorProfileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from emailusernames.utils import create_user
from models import Tutor
from django.conf import settings
from search import strSearchTutors
from django.utils.html import escape
# Create your views here.

def TutorApplication(request, template = 'tutors/tutor_application.html'):
    if not settings.OPEN_SIGNUP:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        user_creation_form = EmailUserCreationForm(request.POST)
        profile_creation_form = ApplicationForm(request.POST)

        if user_creation_form.is_valid() and profile_creation_form.is_valid():
            # Create the user
            user_data = user_creation_form.cleaned_data
            user = create_user(user_data[ 'email' ], user_data[ 'password1' ])

            try:
                tutors_group = Group.objects.get(name = 'Tutors')
            except Group.DoesNotExist:
                tutors_group = Group.objects.create(name = 'Tutors')

            user.is_staff = False
            user.groups.add(tutors_group)

            profile_data = profile_creation_form.cleaned_data
            user.first_name = profile_data[ 'first_name' ][ 0 ].upper() + profile_data[ 'first_name' ][ 1: ].lower()
            user.last_name = profile_data[ 'last_name' ][ 0 ].upper() + profile_data[ 'last_name' ][ 1: ].lower()
            user.save()

            # Create the tutor profile
            tutor = Tutor.objects.create(
                name = user.get_full_name(),
                email = user.email,
                phone = profile_data[ 'phone' ],
                qualifications = profile_data[ 'qualifications' ],
                rate = profile_data[ 'rate' ],
                auth = user,
            )
            for course in profile_data[ 'taught_courses' ]:
                tutor.taught_courses.add(course)
            tutor.save()

            messages.add_message(request, messages.INFO,
                                 'Your application has been successfully received and is pending approval. Thank you '
                                 'for applying for Skule Tutors.')
            return HttpResponseRedirect('/')
    else:
        user_creation_form = EmailUserCreationForm()
        profile_creation_form = ApplicationForm()

    return render_to_response(template,
                              dict(user_creation_form = user_creation_form,
                                   profile_creation_form = profile_creation_form),
                              context_instance = RequestContext(request))

@login_required()
def TutorProfileEdit(request, template = 'tutors/tutor_profile_edit.html'):
    tutor = Tutor.objects.get(auth = request.user)
    if request.method == 'POST':
        profile_form = TutorProfileForm(request.POST)
        if profile_form.is_valid():
            form_data = profile_form.cleaned_data
            tutor.name = form_data['name']
            tutor.email = form_data['email']
            tutor.phone = form_data['phone']
            tutor.qualifications = form_data['qualifications']
            tutor.taught_courses = form_data['taught_courses']
            tutor.rate = form_data['rate']
            tutor.save()
            messages.add_message(request, messages.INFO,
                                 'Your profile has been successfully edited.')
            return HttpResponseRedirect('/')
    else:
        profile_form = TutorProfileForm(tutor.POST_data())
    password_change_form = PasswordChangeForm(user=request.user)
    return render_to_response(template,
                              {'profile_form': profile_form,
                               'password_change_form': password_change_form},
                              context_instance = RequestContext(request))

def SearchTutors(request, template = 'tutors/search.html'):
    if request.GET.get('search'):
        search_terms = escape(request.GET.get('search'))

        result = strSearchTutors(search_terms)

        return render_to_response(template, {'Tutor_list': result, 'query': search_terms},
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/')
