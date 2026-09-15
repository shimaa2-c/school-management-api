from rest_framework.response import Response


def success_response(
    data=None,
    message="Request successful.",
    status=200,
    request=None,
    pagination=None,
):
    request_id = None

    if request is not None:
        request_id = getattr(
            request,
            "request_id",
            None,
        )

    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
            "errors": None,
            "meta": {
                "request_id": request_id,
                "pagination": pagination,
            },
        },
        status=status,
    )


class CustomResponseMixin:

    success_messages = {
        "list": "Resources retrieved successfully.",
        "retrieve": "Resource retrieved successfully.",
        "create": "Resource created successfully.",
        "update": "Resource updated successfully.",
        "partial_update": "Resource updated successfully.",
        "destroy": "Resource deleted successfully.",
    }

    def get_success_message(self, action):
        return self.success_messages.get(
            action,
            "Request successful.",
        )

    def success_response(
        self,
        data=None,
        message="Request successful.",
        status=200,
        pagination=None,
    ):
        return success_response(
            data=data,
            message=message,
            status=status,
            request=self.request,
            pagination=pagination,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
            )

            pagination_data = {
                "count": self.paginator.page.paginator.count,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
            }

            return self.success_response(
                data=serializer.data,
                message=self.get_success_message("list"),
                pagination=pagination_data,
            )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return self.success_response(
            data=serializer.data,
            message=self.get_success_message("list"),
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return self.success_response(
            data=serializer.data,
            message=self.get_success_message("retrieve"),
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_create(serializer)

        return self.success_response(
            data=serializer.data,
            message=self.get_success_message("create"),
            status=201,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop(
            "partial",
            False,
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_update(serializer)

        return self.success_response(
            data=serializer.data,
            message=self.get_success_message(
                "partial_update" if partial else "update"
            ),
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            status=204,
        )