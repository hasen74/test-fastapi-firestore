import cachecontrol
import requests

from fastapi import Request
from fastapi.openapi.models import SecuritySchemeType
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase

from pydantic import BaseModel, Field

from google.oauth2 import id_token
import google.auth.transport.requests


def get_authorization_scheme_param(
    authorization_header_value: str | None,
) -> tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


class SecurityBase(BaseModel):
    type_: SecuritySchemeType = Field(alias="type")
    description: str | None = None

    class Config:
        extra = "allow"


class HTTPBaseModel(SecurityBase):
    type_ = Field(SecuritySchemeType.http, alias="type")
    scheme: str


class HTTPBearer(HTTPBase):
    def __init__(
        self,
        *,
        scheme: str,
        header: str,
        description: str | None = None,
        scheme_name: str | None = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBaseModel(scheme=scheme, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.header = header
        self.auto_error = auto_error

    async def __call__(
            self, request: Request
            ) -> HTTPAuthorizationCredentials | None:
        authorization = request.headers.get(self.header)
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            return None
        if scheme.lower() != "bearer":
            return None
        return HTTPAuthorizationCredentials(
            scheme=scheme, credentials=credentials
        )


oauth2_scheme = HTTPBearer(scheme="Bearer", header="Authorization")


def verify_token(credential: str) -> str:
    try:
        session = requests.session()
        cached_session = cachecontrol.CacheControl(session)
        request = google.auth.transport.requests.Request(
            session=cached_session
        )
        user = id_token.verify_oauth2_token(
            credential,
            request
        )
        print("in verify")
        return user
    except ValueError:
        import traceback
        print(traceback.format_exc())
        return "unauthorized"
