from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_params = "per_page"
    max_page_size = 10000
