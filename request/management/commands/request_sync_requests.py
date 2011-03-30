import logging
import lockfile

from django.core.management import base
from optparse import make_option
from django.conf import settings

from request.log import save_hits

logger = logging.getLogger('djangoproject.request.request_sync_requests')

class Command(base.NoArgsCommand):
    option_list = base.NoArgsCommand.option_list + (
        make_option('-s', action='store_true', dest='silentmode',
            default=False, help='Run in silent mode'),
        make_option('--debug', action='store_true',
            dest='debugmode', default=False,
            help='Debug mode (overrides silent mode)'),
    )

    def handle_noargs(self, **options):
        if not options['silentmode']:
            logging.getLogger('djangoproject').setLevel(logging.INFO)
        if options['debugmode']:
            logging.getLogger('djangoproject').setLevel(logging.DEBUG)
        
        lock = lockfile.FileLock('/tmp/request_sync_request')
        lock.acquire(10)
        with lock:
            logger.info("Saving requests to the database")
            save_hits()
            logger.info("Saving requests to the database")
            
