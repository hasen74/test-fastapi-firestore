from fastapi import FastAPI, HTTPException
from database import db

app = FastAPI()


@app.get("/snippets/{id}")
def get_item(id):
    doc_ref = db.collection("snippets").document(id)
    doc = doc_ref.get()
    snippet = doc.to_dict()
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found.")
    return snippet


@app.get("/snippets")
async def root():
    snippets = db.collection("snippets").stream()
    if not snippets:
        raise HTTPException(status_code=404, detail="Snippets not found.")

    results = []
    for snippet in snippets:
        snippet_data = snippet.to_dict()
        snippet_data["id"] = snippet.id
        results.append(snippet_data)

    return results
