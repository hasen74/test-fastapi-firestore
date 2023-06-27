from fastapi import APIRouter, HTTPException, status
from src.database import db
from datetime import datetime
from src.tags.models import TagBase, TagGet, TagUpdate

router = APIRouter()


# Get all tags
@router.get("/tags", response_model=list[TagGet], tags=["tags"])
async def get_all_tags():

    tags_ref = db.collection("tags")
    query = tags_ref
    docs = query.stream()
    doc_list = list(docs)

    if len(doc_list) == 0:
        raise HTTPException(status_code=404, detail="Tags not found.")

    tags = []
    for doc in doc_list:
        tag = doc.to_dict()
        tag["id"] = doc.id
        tags.append(tag)
    return tags


# Get one tag by id
@router.get("/tags/{id}", response_model=TagGet, tags=["tags"])
async def get_tag(id: str):
    doc_ref = db.collection("tags").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Tag not found.")

    tag = doc.to_dict()
    tag["id"] = id
    return tag


# Create a tag
@router.post(
    "/tags/",
    status_code=status.HTTP_201_CREATED,
    response_model=TagGet,
    tags=["tags"]
    )
async def create_tag(tagCreate: TagBase):
    try:
        tagCreate.createdAt = datetime.utcnow()
        create_time, doc_ref = db.collection("tags").add(
            tagCreate.dict()
        )
        new_tag = TagGet(id=doc_ref.id, **tagCreate.dict())
        return new_tag

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding tag: {str(e)}"
        )


# Delete a tag by id
@router.delete(
  "/tags/{id}",
  response_model=TagGet,
  tags=["tags"]
  )
async def delete_tag(id: str):
    try:
        doc_ref = db.collection("tags").document(id)
        tag_to_delete = doc_ref.get().to_dict()
        doc_ref.delete()
        deleted_tag = TagGet(id=doc_ref.id, **tag_to_delete)
        return deleted_tag

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting tag: {str(e)}"
        )


# Update a tag by id
@router.put("/tags/{id}", response_model=TagGet, tags=["tags"])
async def update_tag(id: str, tagUpdate: TagUpdate):
    try:
        doc_ref = db.collection("tags").document(id)
        original_tag_data = doc_ref.get().to_dict()
        original_tag_model = TagUpdate(**original_tag_data)
        update_data = tagUpdate.dict(exclude_unset=True)
        updated_tag = original_tag_model.copy(update=update_data)
        updated_tag.updatedAt = datetime.utcnow()
        doc_ref.update(updated_tag.dict())

        updated_doc = doc_ref.get()
        final_tag = updated_doc.to_dict()
        final_tag["id"] = id

        return final_tag

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tag: {str(e)}"
        )
