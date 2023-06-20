from fastapi import APIRouter, HTTPException, status
from database import db
from datetime import datetime
from comments.models import CommentBase, CommentGet, CommentUpdate

router = APIRouter()


# Get all comments
@router.get("/comments", response_model=list[CommentGet], tags=["comments"])
async def get_all_comments():

    comments_ref = db.collection("comments")
    query = comments_ref
    docs = query.stream()
    doc_list = list(docs)

    if len(doc_list) == 0:
        raise HTTPException(status_code=404, detail="Comments not found.")

    comments = []
    for doc in doc_list:
        comment = doc.to_dict()
        comment["id"] = doc.id
        comments.append(comment)
    return comments


# Get one comment by id
@router.get("/comments/{id}", response_model=CommentGet, tags=["comments"])
async def get_comment(id: str):
    doc_ref = db.collection("comments").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Comment not found.")

    comment = doc.to_dict()
    comment["id"] = id
    return comment


# Create a comment
@router.post(
    "/comments/",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentGet,
    tags=["comments"]
    )
async def create_comment(commentCreate: CommentBase):
    try:
        commentCreate.createdAt = datetime.utcnow()
        create_time, doc_ref = db.collection("comments").add(
            commentCreate.dict()
        )
        new_comment = CommentGet(id=doc_ref.id, **commentCreate.dict())
        return new_comment

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding comment: {str(e)}"
        )


# Delete a comment by id
@router.delete(
  "/comments/{id}",
  response_model=CommentGet,
  tags=["comments"]
  )
async def delete_comment(id: str):
    try:
        doc_ref = db.collection("comments").document(id)
        comment_to_delete = doc_ref.get().to_dict()
        doc_ref.delete()
        deleted_comment = CommentGet(id=doc_ref.id, **comment_to_delete)
        return deleted_comment

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting comment: {str(e)}"
        )


# Update a comment by id
@router.put("/comments/{id}", response_model=CommentGet, tags=["comments"])
async def update_comment(id: str, commentUpdate: CommentUpdate):
    try:
        doc_ref = db.collection("comments").document(id)
        original_comment_data = doc_ref.get().to_dict()
        original_comment_model = CommentUpdate(**original_comment_data)
        update_data = commentUpdate.dict(exclude_unset=True)
        updated_comment = original_comment_model.copy(update=update_data)
        updated_comment.updatedAt = datetime.utcnow()
        doc_ref.update(updated_comment.dict())

        updated_doc = doc_ref.get()
        final_comment = updated_doc.to_dict()
        final_comment["id"] = id

        return final_comment

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating comment: {str(e)}"
        )
