from fastapi import APIRouter, HTTPException
from database import db

router = APIRouter()


@router.get("/snippets/{id}")
def get_item(id):
    doc_ref = db.collection("snippets").document(id)
    doc = doc_ref.get()
    snippet = doc.to_dict()
    snippet["id"] = id
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found.")
    return snippet


@router.get("/snippets")
async def root():
    docs = db.collection("snippets").stream()
    if not docs:
        raise HTTPException(status_code=404, detail="Snippets not found.")

    snippets = []
    for doc in docs:
        snippet = doc.to_dict()
        snippet["id"] = doc.id
        snippets.append(snippet)

    return snippets
