import logging
from threading import Thread
from django.core import management
from django.contrib.sessions.models import Session


def cleaner():
    logging.debug("Thread session cleaner Start")
    management.call_command('clearsessions')
    logging.debug("Thread session cleaner Finish")


def shop_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        length = Session.objects.count()
        if length >= 1000 and request.META.get('path_info'.upper()) == '/':
            cs = Thread(target=cleaner)
            cs.start()
            status_name = 'DAEMON' if cs.daemon else ''
            logging.debug(f'({cs.name}) ID:{cs.ident} status: %s', status_name)

        return response

    return middleware
