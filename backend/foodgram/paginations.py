from rest_framework import pagination


class RecipePageNumberPagination(pagination.PageNumberPagination):
    """Custom paginator that accepts the limit parameter in the request"""

    page_size_query_param = 'limit'
