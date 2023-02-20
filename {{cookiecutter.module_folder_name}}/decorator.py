from datetime import timedelta
from functools import wraps

from .serialization import GzipSerializer, hash_args


class ExpiringCache:
    serializer = GzipSerializer()

    def __init__(self, backend, default_ttl=timedelta(seconds=60)):
        self.backend = backend
        self.default_ttl = default_ttl

    def __call__(self, ttl: timedelta = None):
        if not ttl:
            ttl = self.default_ttl

        def decorator(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                function_name = f"{func.__module__}.{func.__name__}"
                hashkey = hash_args(function_name, *args, **kwargs)
                raw_value = self.backend.get(hashkey)

                if raw_value:
                    return self.serializer.unmarshal(raw_value)

                results = func(*args, **kwargs)

                self.backend.save(
                    hashkey, self.serializer.marshal(results), ttl
                )

                return results
            return wrapped
        return decorator
