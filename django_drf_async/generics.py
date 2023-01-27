from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.settings import api_settings

from django_drf_async import mixins
from django_drf_async.api_view import AsyncAPIView


class AsyncGenericAPIView(AsyncAPIView):
    """
    A base view for asynchronous generic views.
    """

    queryset = None
    serializer_class = None
    lookup_field = "pk"
    lookup_url_kwarg = None
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (E.g. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method." % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    async def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = await sync_to_async(self.filter_queryset)(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = await sync_to_async(get_object_or_404)(queryset, **filter_kwargs)

        # May raise a permission denied
        await sync_to_async(self.check_object_permissions)(self.request, obj)
        return obj

    async def get_serializer(self, *args, **kwargs):
        """
        Return the async serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    async def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return await self.paginator.paginate_queryset(queryset, self.request, view=self)

    async def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return await self.paginator.get_paginated_response(data)


class AsyncCreateAPIView(mixins.AsyncCreateModelMixin, AsyncGenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    async def post(self, request, *args, **kwargs):
        return await self.create(request, *args, **kwargs)


class AsyncListAPIView(mixins.AsyncListModelMixin, AsyncGenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    async def get(self, request, *args, **kwargs):
        return await self.list(request, *args, **kwargs)


class AsyncRetrieveAPIView(mixins.AsyncRetrieveModelMixin, AsyncGenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """

    async def get(self, request, *args, **kwargs):
        return await self.retrieve(request, *args, **kwargs)


class AsyncDestroyAPIView(mixins.AsyncDestroyModelMixin, AsyncGenericAPIView):
    """
    Concrete view for deleting a model instance.
    """

    async def delete(self, request, *args, **kwargs):
        return await self.destroy(request, *args, **kwargs)


class AsyncUpdateAPIView(mixins.AsyncUpdateModelMixin, AsyncGenericAPIView):
    """
    Concrete view for updating a model instance.
    """

    async def put(self, request, *args, **kwargs):
        return await self.update(request, *args, **kwargs)

    async def patch(self, request, *args, **kwargs):
        return await self.partial_update(request, *args, **kwargs)
