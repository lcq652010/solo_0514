from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        page_number = request.query_params.get(self.page_query_param, 1)
        try:
            page_number = int(page_number)
            if page_number < 1:
                page_number = 1
        except (ValueError, TypeError):
            page_number = 1

        paginator = self.django_paginator_class(queryset, page_size)
        
        try:
            self.page = paginator.page(page_number)
        except NotFound:
            self.page = paginator.page(paginator.num_pages) if paginator.num_pages > 0 else paginator.page(1)

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'items': data,
                'total': self.page.paginator.count,
                'page': self.page.number,
                'page_size': self.page.paginator.per_page,
                'total_pages': self.page.paginator.num_pages,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
            }
        })