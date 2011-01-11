import datetime

from django.core.urlresolvers import get_callable

from request.models import Request
from request import settings
from request.router import patterns

class RequestMiddleware(object):
    def process_response(self, request, response):
        if response.status_code < 400 and settings.REQUEST_ONLY_ERRORS:
            return response
        
        ignore = patterns(False, *settings.REQUEST_IGNORE_PATHS)
        if ignore.resolve(request.path[1:]):
            return response
        
        if request.is_ajax() and settings.REQUEST_IGNORE_AJAX:
            return response
        
        if request.META.get('REMOTE_ADDR') in settings.REQUEST_IGNORE_IP:
            return response
        
        if getattr(request, 'user', False):
            if request.user.username in settings.REQUEST_IGNORE_USERNAME:
                return response
        
        if not getattr(request, 'session', None):
            return response

        r = Request()
        now = datetime.datetime.now()
        path = request.path
        if path[len(path)-1] != '/':
            path = path + '/'
    
        if path in settings.REQUEST_ALWAYS_INSERT_FROM_URLS:
            try:
                request.session['last_request_log'] = now
            except:
                pass
            r.from_http_request(request, response)        
            return response

        try:
            last_log = request.session['last_request_log']
            last_log_limit = last_log + \
                settings.REQUEST_USER_TRACKING_LOGAGAIN_DELAY
            if now < last_log_limit :
                return response
        except KeyError:
            pass 
        request.session['last_request_log'] = now
        r.from_http_request(request, response)        
        return response
