from math import ceil
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Custom pagination class
class CustomPagination(PageNumberPagination):
    page_size = 5  # Set default page size
    page_size_query_param = 'page_size'  # Allow clients to set their own page size

    def get_paginated_response(self, data):
        # Calculate the total number of pages
        last_page = ceil(self.page.paginator.count / self.page_size)

        return Response({
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'last_page': last_page,
            'results': data,
        })