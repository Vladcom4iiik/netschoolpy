"""netschoolpy — асинхронный клиент для «Сетевого города»."""

from .client import NetSchool, search_schools
from .exceptions import (
    ESIAError,
    LoginError,
    MFAError,
    NetSchoolError,
    SchoolNotFound,
    ServerUnavailable,
    SessionExpired,
)
from .regions import REGIONS, get_url, list_regions

__version__ = "3.0.0"

__all__ = [
    "NetSchool",
    "search_schools",
    "NetSchoolError",
    "LoginError",
    "MFAError",
    "ESIAError",
    "SchoolNotFound",
    "SessionExpired",
    "ServerUnavailable",
    "REGIONS",
    "get_url",
    "list_regions",
]
