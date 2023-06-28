import cachecontrol
import google.auth.transport.requests
import requests
from typing import NoReturn

from fastapi import HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2 import id_token


oauth2_scheme = HTTPBearer()


def raise_401() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized.",
    )


def raise_403() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden.",
    )


# Authorization dependency injected in api routes
def get_current_user(
    creds: HTTPAuthorizationCredentials = Security(oauth2_scheme)
):
    user_email = verify_token(creds.credentials)['email']
    return user_email


# Google idtoken verification with cache
def verify_token(token: str) -> str:
    try:
        session = requests.session()
        cached_session = cachecontrol.CacheControl(session)
        request = google.auth.transport.requests.Request(
            session=cached_session
        )
        user = id_token.verify_oauth2_token(
            token,
            request
        )
        return user
    except ValueError:
        import traceback
        print(traceback.format_exc())
        return "Unauthorized"
