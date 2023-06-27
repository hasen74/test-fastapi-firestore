from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from src.snippets.router import router as snippets_router
from src.users.router import router as users_router
from src.languages.router import router as languages_router
from src.tags.router import router as tags_router
from src.comments.router import router as comments_router
from src.notifications.router import router as notifications_router
from src.dependencies import oauth2_scheme, verify_token

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint
)
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette_context import context
from starlette_context.middleware import RawContextMiddleware


app = FastAPI()


class JwtAccessMiddleware(BaseHTTPMiddleware):
    """JWT Access Middleware"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> StreamingResponse:
        cred: HTTPAuthorizationCredentials | None = await oauth2_scheme(
            request
        )
        if cred:
            context["USER_ID"] = verify_token(cred.credentials)
            print("in middleware")
            print(context["USER_ID"])
            # logger.info(f"Request by {context.get('USER_ID')}")
        else:
            response = call_next(request)
        return response


app.include_router(snippets_router)
app.include_router(users_router)
app.include_router(languages_router)
app.include_router(tags_router)
app.include_router(comments_router)
app.include_router(notifications_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ExceptionMiddleware)
app.add_middleware(JwtAccessMiddleware)
app.add_middleware(RawContextMiddleware)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
