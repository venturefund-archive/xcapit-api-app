from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
import urllib.parse as urlparse


class CustomCursorPaginationAPU(CursorPagination):
    ordering = ['created_at', ]

    def __init__(self, ordering=None):
        if ordering:
            self.ordering = ordering
        super(CustomCursorPaginationAPU, self).__init__()

    def get_cursor(self, direction):
        if direction == 'next':
            url = self.get_next_link()
        elif direction == 'previous':
            url = self.get_previous_link()
        else:
            return None
        parsed = urlparse.urlparse(url)
        parsed_qs = urlparse.parse_qs(parsed.query)
        if 'cursor' in parsed_qs:
            return parsed_qs['cursor'][0]
        else:
            return None

    def get_paginated_response(self, data):

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'cursors': {
                'next': self.get_cursor('next'),
                'previous': self.get_cursor('previous')
            },
            'results': data
        })


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
