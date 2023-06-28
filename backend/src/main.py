from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from src.snippets.router import router as snippets_router
from src.users.router import router as users_router
from src.languages.router import router as languages_router
from src.tags.router import router as tags_router
from src.comments.router import router as comments_router
from src.notifications.router import router as notifications_router


app = FastAPI()


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


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
