from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size =1
    page_size_query_params = "count"
    maximum_page_size =5
    page_query_param = "p"