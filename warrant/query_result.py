from warrant import Warrant
from typing import Any, Dict


class QueryResult:
    def __init__(self, object_type: str, object_id: str, warrant: Warrant, is_implicit: bool, meta: Dict[str, Any] = {}):
        self.object_type = object_type
        self.object_id = object_id
        self.warrant = warrant
        self.is_implicit = is_implicit
        self.meta = meta
