import json
import logging


class JsonRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.JSON = {}

        ctype = request.META.get('CONTENT_TYPE', '')
        if ctype.lower().find('json') >= 0:
            request.JSON = self.process_json_request(request)

        #
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_json_request(self, request):
        body = request.body.decode('utf-8')
        try:
            return json.loads(body)
        except Exception as e:
            logging.exception(e)
        return {}

