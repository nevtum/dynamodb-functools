import gzip
import hashlib
import json
import pickle
from base64 import b64decode, b64encode
from typing import Any


def hash_args(function_name, *args, **kwargs) -> str:
    data = json.dumps({
        "func_name": function_name,
        "args": args,
        "kwargs": kwargs
    })
    hash_value = hashlib.sha1(data.encode())
    return hash_value.hexdigest()


class GzipSerializer:
    def marshal(self, results: Any) -> bytes:
        a_bytes = pickle.dumps(results)
        return b64encode(gzip.compress(a_bytes))

    def unmarshal(self, raw_value: bytes) -> Any:
        a_bytes = gzip.decompress(b64decode(raw_value))
        return pickle.loads(a_bytes)
