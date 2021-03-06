import os
import dj_database_url

# Django settings for skule_tutors2 project.

DEBUG = eval(os.environ.get('DJANGO_DEBUG', 'True'))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Oliver Liang', 'oliver.liang@mail.utoronto.ca'),
    )

MANAGERS = ADMINS

DATABASES = {}

if os.getenv('DATABASE_URL'):
    DATABASES[ 'default' ] = dj_database_url.config()
else:
    DATABASES[ 'default' ] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd7mgc0d7rai4lt',
        'HOST': 'ec2-54-243-227-29.compute-1.amazonaws.com',
        'PORT': 5432,
        'USER': 'saybdxcpuwfnhd',
        'PASSWORD': 'g-ZnCoTMb0orDk7VKjoBW4DnOJ'}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Toronto'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media').replace('\\', '/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# Serve file from STATIC_ROOT only if debug is false
if DEBUG:
    STATIC_ROOT = ''
else:
    STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static').replace('\\', '/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

# Serve files from STATICFILES_DIRS only if DEBUG is turned on
if DEBUG:
    STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), 'static').replace('\\', '/'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',
                       'NxG6PeAtVG9n776UiHGqlsWOTR7aqVNBbtfEIhaIoeRSZQcYJv_EU'
                       'chsZd5zltERoLooRu0O2OTcGFSH4pcAxZcVjKrYmPTHd')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',

    #installed apps
    'emailusernames',
    'south',

    #skule apps
    'tutors',
    'course_manage',
    )

# Install gunicorn if it's available as a package
# to allow development on windows machines
try:
    import gunicorn
    INSTALLED_APPS += ('gunicorn',)
except ImportError, e:
    pass

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': [ 'mail_admins' ],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# email settings

if os.getenv('SMTPSERVER'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('SMTPSERVER')
    EMAIL_HOST_USER = os.getenv('SMTPUSER')
    EMAIL_HOST_PASSWORD = os.getenv('SMTPPASS')
    EMAIL_PORT = int(os.getenv('SMTPPORT'))
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025

#django-email-as-username settings
AUTHENTICATION_BACKENDS = (
    'emailusernames.backends.EmailAuthBackend',
    )

LOGIN_REDIRECT_URL = '/'

OPEN_SIGNUP = True
