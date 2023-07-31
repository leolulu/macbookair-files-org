from dataclasses import dataclass, field
from typing import Callable, List, Optional

import dill


@dataclass(frozen=False)
class WhisperTask:
    media_path: str
    verbose: Optional[bool] = False
    target_languages: Optional[List[str]] = None
    post_func: Optional[Callable] = None
    post_func_bytes: Optional[bytes] = field(init=False)

    def __post_init__(self):
        if self.post_func:
            self.post_func_bytes = dill.dumps(self.post_func)
        else:
            self.post_func_bytes = None
        del self.post_func
