# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from snippets.router import router as snippets_router
from users.router import router as users_router
from languages.router import router as languages_router
from tags.router import router as tags_router
from comments.router import router as comments_router
from session import router as session_router
from notifications.router import router as notifications_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(snippets_router)
app.include_router(users_router)
app.include_router(languages_router)
app.include_router(tags_router)
app.include_router(comments_router)
app.include_router(notifications_router)
app.include_router(session_router)

# if __name__ == "__main__":
# #     uvicorn.run(app, host="0.0.0.0", port=8000)
