from typing import Generator, List

from src.models import Event
from src.repository import AbstractRepository


class BaseUnitOfWork:
    def __init__(self, *args, **kwargs):
        """Instantiate Unit of Work - arguments are passed into constructors of
        repositories"""
        # Instantiate repositories
        self._repositories = {
            k: v(*args, **kwargs) for k, v in self._repositories.items()
        }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls._repositories = {
            k: v for k, v in kwargs.items() if issubclass(v, AbstractRepository)
        }

    async def __aenter__(self) -> "BaseUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # If transaction is committed, rollback shouldn't error
        # This is here as a fallback
        await self.rollback()

    def __getattr__(self, item: str) -> AbstractRepository:
        # Enable accessing repositories as attributes
        # E.g. uow.customers.add()
        return self._repositories[item]

    def collect_new_events(self) -> Generator[List[Event], None, None]:
        for repository in self._repositories.values():
            for entity in repository.seen:
                while entity.events:
                    yield entity.events.pop(0)

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
