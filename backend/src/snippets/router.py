from fastapi import APIRouter, HTTPException, status
from database import db
from datetime import datetime
from snippets.models import SnippetBase, SnippetGet, SnippetUpdate

router = APIRouter()


@router.get("/snippets", response_model=list[SnippetGet], tags=['snippets'])
async def get_all_snippets():
    docs = db.collection("snippets").stream()
    doc_list = list(docs)
    if len(doc_list) == 0:
        raise HTTPException(status_code=404, detail="Snippets not found.")
    snippets = []
    for doc in docs:
        snippet = doc.to_dict()
        snippet["id"] = doc.id
        snippets.append(snippet)

    return snippets


@router.get("/snippets/{id}", response_model=SnippetGet, tags=['snippets'])
async def get_snippet(id: str):
    doc_ref = db.collection("snippets").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Snippet not found.")
    snippet = doc.to_dict()
    snippet["id"] = id
    return snippet


@router.post("/snippets/", status_code=status.HTTP_201_CREATED, tags=['snippets'])
async def create_snippet(snippetCreate: SnippetBase):
    snippetCreate.createdAt = datetime.utcnow()
    create_time, doc_ref = db.collection("snippets").add(snippetCreate.dict())
    return (f"Snippet Id {doc_ref.id} created successfully")


@router.delete("/snippets/{id}", tags=['snippets'])
async def delete_snippet(id: str):
    doc_ref = db.collection("snippets").document(id)
    doc_ref.delete()
    return (f"Snippet Id {doc_ref.id} deleted successfully")


@router.put("/snippets/{id}", tags=['snippets'])
async def update_snippet(id: str, snippetUpdate: SnippetUpdate):
    doc_ref = db.collection("snippets").document(id)
    original_snippet_data = doc_ref.get().to_dict()
    original_snippet_model = SnippetUpdate(**original_snippet_data)
    update_data = snippetUpdate.dict(exclude_unset=True)
    updated_snippet = original_snippet_model.copy(update=update_data)
    updated_snippet.updatedAt = datetime.utcnow()
    doc_ref.update(updated_snippet.dict())
    new_ref = db.collection("snippets").document(id)
    return (new_ref.get().to_dict())
