import datetime

from django.conf import settings
from django.contrib.sites.models import Site

REQUEST_ALWAYS_INSERT_FROM_URLS = getattr(settings, 
                            'REQUEST_ALWAYS_INSERT_FROM_URLS', [])
REQUEST_ONLY_ERRORS = getattr(settings, 'REQUEST_ONLY_ERRORS', False)
REQUEST_IGNORE_AJAX = getattr(settings, 'REQUEST_IGNORE_AJAX', False)
REQUEST_IGNORE_IP = getattr(settings, 'REQUEST_IGNORE_IP', tuple())
REQUEST_IGNORE_USERNAME = getattr(settings, 'REQUEST_IGNORE_USERNAME', tuple())
REQUEST_IGNORE_PATHS = getattr(settings, 'REQUEST_IGNORE_PATHS', tuple())
REQUEST_USER_TRACKING_LOGAGAIN_DELAY = getattr(settings, 
    'REQUEST_USER_TRACKING_LOGAGAIN_DELAY', datetime.timedelta(minutes=3))
REQUEST_USE_HOSTED_MEDIA = getattr(settings, 'REQUEST_USE_HOSTED_MEDIA', True)
REQUEST_MEDIA_PREFIX = getattr(settings, 'REQUEST_MEDIA_PREFIX', settings.MEDIA_URL)

REQUEST_TRAFFIC_MODULES = getattr(settings, 'REQUEST_TRAFFIC_MODULES', (
    'request.traffic.UniqueVisitor',
    'request.traffic.UniqueVisit',
    'request.traffic.Hit',
))

REQUEST_PLUGINS = getattr(settings, 'REQUEST_PLUGINS', (
    'request.plugins.TrafficInformation',
    'request.plugins.LatestRequests',
    
    'request.plugins.TopPaths',
    'request.plugins.TopErrorPaths',
    'request.plugins.TopReferrers',
    'request.plugins.TopSearchPhrases',
    'request.plugins.TopBrowsers',
))

try:
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://%s' % Site.objects.get_current().domain)
except:
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://127.0.0.1')
