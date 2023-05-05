from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response


class PageNumberPaginationView(PageNumberPagination):

    """override this method to change the response """
    def get_paginated_response(self, data):
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "count" : self.page.paginator.count,
            "next" : self.get_next_link(),
            "previous" : self.get_previous_link(),
            "pages" : self.page.paginator.num_pages,
            "data" : data
        }
        return Response(response, status=status.HTTP_200_OK)
