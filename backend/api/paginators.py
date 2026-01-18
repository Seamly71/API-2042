from rest_framework.pagination import PageNumberPagination

from api.constants import DEFAULT_PAGINATION_PAGE_SIZE


class APIPagination(PageNumberPagination):
    page_size = DEFAULT_PAGINATION_PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'limit'