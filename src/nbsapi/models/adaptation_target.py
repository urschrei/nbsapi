from functools import wraps
from typing import List

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from nbsapi.database import get_db_session

from . import Base


def _unique(session, cls, hashfunc, queryfunc, constructor, arg, kw):
    cache = getattr(session, "_unique_cache", None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, hashfunc(*arg, **kw))
    if key in cache:
        return cache[key]
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, *arg, **kw)
            obj = q.first()
            if not obj:
                obj = constructor(*arg, **kw)
                session.add(obj)
        cache[key] = obj
        return obj


def unique_constructor(scoped_session, hashfunc, queryfunc):
    def decorate(cls):
        def _null_init(self, *arg, **kw):
            pass

        @wraps(cls)
        def __new__(cls, bases, *arg, **kw):
            # no-op __new__(), called
            # by the loading procedure
            if not arg and not kw:
                return object.__new__(cls)

            session = scoped_session()

            def constructor(*arg, **kw):
                obj = object.__new__(cls)
                obj._init(*arg, **kw)
                return obj

            return _unique(session, cls, hashfunc, queryfunc, constructor, arg, kw)

        # note: cls must be already mapped for this part to work
        cls._init = cls.__init__
        cls.__init__ = _null_init
        cls.__new__ = classmethod(__new__)
        return cls

    return decorate


@unique_constructor(
    get_db_session(),
    lambda target: target,
    lambda query, target: query.filter(AdaptationTarget.target == target),
)
class AdaptationTarget(Base):
    __tablename__ = "adaptationtarget"
    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[str] = mapped_column(index=True, unique=True)
    solutions: Mapped[List["Association"]] = relationship(
        back_populates="tg", lazy="joined"
    )
