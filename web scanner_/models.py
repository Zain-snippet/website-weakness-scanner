from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class ResponseData:
    input_url: str
    final_url: str
    status_code: int
    headers: Dict[str, str]
    cookies: List[Dict[str, Union[str, bool]]]
    body: Union[str, bytes]
    is_https: bool


@dataclass
class Finding:
    title: str
    status: str          # "present" or "missing"
    severity: str        # "Low" or "Medium"
    description: str
    remediation: str