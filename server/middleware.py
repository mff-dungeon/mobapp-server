import sys
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.utils import termcolors
from django.utils.deprecation import MiddlewareMixin

from server.exceptions import HttpException


class QueryPrintingMiddleware(MiddlewareMixin):
    start = None

    def process_request(self, request):
        if settings.DEBUG:
            self.start = len(connection.queries)

    def process_response(self, request, response):
        if settings.DEBUG and 'runserver' in sys.argv and self.start is not None:
            yellow = termcolors.make_style(opts=('bold',), fg='yellow')

            count = len(connection.queries) - self.start
            output = '# queries: %s' % count
            output = output.ljust(15)

            for q in connection.queries[self.start:]:
                sys.stderr.write(yellow("\t" + q['sql'] + "\n"))

        return response


class HttpExceptionHandler:
    def process_exception(self, request, exception):
        if exception is not HttpException:
            return None

        return JsonResponse({
            'message': exception.message
        }, status=exception.status_code)
