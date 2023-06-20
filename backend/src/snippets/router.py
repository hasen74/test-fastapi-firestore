from fastapi import APIRouter, HTTPException, status
from database import db
from datetime import datetime
from snippets.models import SnippetBase, SnippetGet, SnippetUpdate

router = APIRouter()


# Get all snippets with search options (query params)
@router.get("/snippets", response_model=list[SnippetGet], tags=["snippets"])
async def get_all_snippets(
    tag: str | None = None,
    lang: str | None = None,
    user: str | None = None
):

    # Get the collection ref and filter by language and tag if provided
    snippets_ref = db.collection("snippets")
    query = snippets_ref
    if lang:
        query = query.where("language_id", "==", lang)
    if tag:
        query = query.where("tags", "array_contains", tag)
    if user:
        query = query.where("user_email", "==", user)

    # Use of stream() generator to iterate through results
    docs = query.stream()
    doc_list = list(docs)

    if len(doc_list) == 0:
        raise HTTPException(status_code=404, detail="Snippets not found.")

    snippets = []
    for doc in doc_list:
        snippet = doc.to_dict()
        snippet["id"] = doc.id
        snippets.append(snippet)
    return snippets


# Get one snippet by id
@router.get("/snippets/{id}", response_model=SnippetGet, tags=["snippets"])
async def get_snippet(id: str):
    doc_ref = db.collection("snippets").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Snippet not found.")

    snippet = doc.to_dict()
    snippet["id"] = id
    return snippet


# Create a snippet
@router.post(
    "/snippets/",
    status_code=status.HTTP_201_CREATED,
    response_model=SnippetGet,
    tags=["snippets"]
    )
async def create_snippet(snippetCreate: SnippetBase):
    try:
        snippetCreate.createdAt = datetime.utcnow()
        create_time, doc_ref = db.collection("snippets").add(
            snippetCreate.dict()
        )
        new_snippet = SnippetGet(id=doc_ref.id, **snippetCreate.dict())
        return new_snippet

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding snippet: {str(e)}"
        )


# Delete a snippet by id
@router.delete("/snippets/{id}", response_model=SnippetGet, tags=["snippets"])
async def delete_snippet(id: str):
    try:
        doc_ref = db.collection("snippets").document(id)
        snippet_to_delete = doc_ref.get().to_dict()
        doc_ref.delete()
        deleted_snippet = SnippetGet(id=doc_ref.id, **snippet_to_delete)
        return deleted_snippet

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting snippet: {str(e)}"
        )


# Update a snippet by id
@router.put("/snippets/{id}", response_model=SnippetGet, tags=["snippets"])
async def update_snippet(id: str, snippetUpdate: SnippetUpdate):
    try:
        doc_ref = db.collection("snippets").document(id)
        original_snippet_data = doc_ref.get().to_dict()
        original_snippet_model = SnippetUpdate(**original_snippet_data)
        update_data = snippetUpdate.dict(exclude_unset=True)
        updated_snippet = original_snippet_model.copy(update=update_data)
        updated_snippet.updatedAt = datetime.utcnow()
        doc_ref.update(updated_snippet.dict())

        updated_doc = doc_ref.get()
        final_snippet = updated_doc.to_dict()
        final_snippet["id"] = id

        return final_snippet

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating snippet: {str(e)}"
        )
