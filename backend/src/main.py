# import uvicorn
from fastapi import FastAPI
from snippets.router import router as snippets_router

app = FastAPI()

app.include_router(snippets_router)

# if __name__ == "__main__":
# #     uvicorn.run(app, host="0.0.0.0", port=8000)
