from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class AsyncBaseMixin:
    service_class = None


class AsyncCreateModelMixin(AsyncBaseMixin):
    """
    Create a model instance.
    """

    async def create(self, request, *args, **kwargs):
        serializer = await self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        await self.perform_create(serializer)
        headers = await self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    async def perform_create(self, serializer):
        if not self.service_class:
            raise NotImplementedError("You must define a service class")
        await self.service_class.create(**serializer.validated_data)

    @staticmethod
    async def get_success_headers(data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class AsyncListModelMixin(AsyncBaseMixin):
    """
    List a queryset.
    """

    async def list(self, request, *args, **kwargs):
        queryset = await sync_to_async(list)(self.filter_queryset(self.get_queryset()))

        page = await self.paginate_queryset(queryset)
        if page is not None:
            serializer = await self.get_serializer(page, many=True)
            return await self.get_paginated_response(serializer.data)

        serializer = await self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AsyncRetrieveModelMixin(AsyncBaseMixin):
    """
    Retrieve a model instance.
    """

    async def retrieve(self, request, *args, **kwargs):
        instance = await self.get_object()
        serializer = await self.get_serializer(instance)
        return Response(serializer.data)


class AsyncUpdateModelMixin(AsyncBaseMixin):
    """
    Update a model instance.
    """

    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = await self.get_object()
        serializer = await self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        await self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    async def perform_update(self, serializer):
        await self.service_class.update(
            serializer.instance.id, **serializer.validated_data
        )

    async def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return await self.update(request, *args, **kwargs)


class AsyncDestroyModelMixin(AsyncBaseMixin):
    """
    Destroy a model instance.
    """

    async def destroy(self, request, *args, **kwargs):
        instance = await self.get_object()
        await self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    async def perform_destroy(self, instance):
        await self.service_class.delete(instance.id)
