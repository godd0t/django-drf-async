from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from django.db.models import Model


@dataclass
class BaseService(ABC):
    """
    Base class for all services
    """

    entity: Type[Model]
    lookup_field: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.entity = Type[Model]
        cls.__abstractmethods__ = frozenset()

    @classmethod
    async def get_object(cls, identifier: str = None):
        if identifier:
            return await cls.entity.objects.aget(**{cls.lookup_field: identifier})
        return None


class BaseCreateService(BaseService):
    """
    Base class for all services that create entities
    """

    @classmethod
    @abstractmethod
    async def create(cls, **kwargs) -> Model:
        raise NotImplementedError


class BaseUpdateService(BaseService):
    """
    Base class for all services that update entities
    """

    @classmethod
    @abstractmethod
    async def update(cls, **kwargs) -> Model:
        raise NotImplementedError


class BaseDeleteService(BaseService):
    """
    Base class for all services that delete entities
    """

    @classmethod
    @abstractmethod
    async def delete(cls, **kwargs) -> Model:
        raise NotImplementedError


class BaseRetrieveService(BaseService):
    """
    Base class for all services that retrieve entities
    """

    @classmethod
    @abstractmethod
    async def retrieve(cls, **kwargs) -> Model:
        raise NotImplementedError


class BaseListService(BaseService):
    """
    Base class for all services that list entities
    """

    @classmethod
    @abstractmethod
    async def list(cls, **kwargs) -> Model:
        raise NotImplementedError
