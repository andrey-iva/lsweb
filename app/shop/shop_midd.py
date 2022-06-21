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

        logging.debug("check length session rows for db")
        if len(Session.objects.all()) >= 1000:
        	Thread(target=cleaner).start()

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        

        return response

    return middleware