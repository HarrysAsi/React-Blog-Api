from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class UserLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 4
    max_limit = 4


class PostCommentsPagination(PageNumberPagination):
    page_size = 5
