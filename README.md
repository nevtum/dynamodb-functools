DynamoDB functools
===

The DynamoDB functools cache decorator is a lightweight bit of code to memoize Python functions that are called frequently and are expensive to run. Arguments as well as returned results are cached after the first invocation of a decorated function. It works a lot like Python's own functools decorator `lru_cache` built into the standard library. Difference is this library comes with a powerful and scalable storage backend to cache and expire results as you need.

## How to get set up

In order to use this package the boto3 library must be installed. Generate your code using cookiecutter.

```bash
    $ cookiecutter https://github.com/nevtum/dynamodb-functools.git
```

Then setup your cache decorator to be used to decorate other Python functions.

```python
from my_module import ExpiringCache, DynamoDbBackend

cache = ExpiringCache(
    backend=DynamoDbBackend("my_table")
)
```

Simply reference your cache decorator and decorate functions which you wish to cache results from.
To specify how long you want values to be in cache set the ttl (time to live) variable when applying
the decorator. If no ttl value is specified the default ttl from the expiring cache will be used.

```python
from datetime import timedelta

@cache(ttl=timedelta(minutes=30))
def my_function_to_cache(*args, **kwargs):
    # some expensive operation
    return {
        "args": args,
        "kwargs": kwargs
    }
```
