from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class HttpSnapshot:
    input_url: str
    final_url: str
    status_code: int
    headers: Dict[str, str]
    cookies: List["CookieSnapshot"]
    body: str
    is_https: bool


@dataclass
class CookieSnapshot:
    name: str
    value: str
    secure: bool
    httponly: bool
    samesite: Optional[str]


@dataclass
class FormSnapshot:
    action: str
    method: str
    inputs: List[Dict[str, Optional[str]]]


@dataclass
class Finding:
    title: str
    status: str
    severity: str
    description: str
    remediation: str