from fastapi import APIRouter, HTTPException, status
from database import db
from datetime import datetime
from users.models import UserBase, UserGet, UserUpdate, Token

from google.oauth2 import id_token
import google.auth.transport.requests

import cachecontrol
import requests

router = APIRouter()


# Get all users
@router.get("/users", response_model=list[UserGet], tags=["users"])
def get_all_users():
    users_ref = db.collection("users")
    query = users_ref
    docs = query.stream()
    doc_list = list(docs)

    if len(doc_list) == 0:
        raise HTTPException(status_code=404, detail="Users not found.")

    users = []
    for doc in doc_list:
        user = doc.to_dict()
        user["id"] = doc.id
        users.append(user)
    return users


# Get one user by id
@router.get("/users/{id}", response_model=UserGet, tags=["users"])
def get_user(id: str):
    doc_ref = db.collection("users").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found.")

    user = doc.to_dict()
    user["id"] = id
    return user


# Create a user
@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserGet,
    tags=["users"],
)
def create_user(userCreate: UserBase):
    try:
        userCreate.createdAt = datetime.utcnow()
        create_time, doc_ref = db.collection("users").add(userCreate.dict())
        new_user = UserGet(id=doc_ref.id, **userCreate.dict())
        return new_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding user: {str(e)}",
        )


# Delete a user by id
@router.delete("/users/{id}", response_model=UserGet, tags=["users"])
def delete_user(id: str):
    try:
        doc_ref = db.collection("users").document(id)
        user_to_delete = doc_ref.get().to_dict()
        doc_ref.delete()
        deleted_user = UserGet(id=doc_ref.id, **user_to_delete)
        return deleted_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}",
        )


# Update a user by id
@router.put("/users/{id}", response_model=UserGet, tags=["users"])
def update_user(id: str, userUpdate: UserUpdate):
    try:
        doc_ref = db.collection("users").document(id)
        original_user_data = doc_ref.get().to_dict()
        original_user_model = UserUpdate(**original_user_data)
        update_data = userUpdate.dict(exclude_unset=True)
        updated_user = original_user_model.copy(update=update_data)
        updated_user.updatedAt = datetime.utcnow()
        doc_ref.update(updated_user.dict())

        updated_doc = doc_ref.get()
        final_user = updated_doc.to_dict()
        final_user["id"] = id

        return final_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}",
        )


@router.post("/users/auth", tags=["users"])
def authentication(token: Token):
    try:

        session = requests.session()
        cached_session = cachecontrol.CacheControl(session)
        request = google.auth.transport.requests.Request(
            session=cached_session
        )
        user = id_token.verify_oauth2_token(
            token.token,
            request
        )
        print(user)

        return user["name"] + " Logged In successfully"

    except ValueError:
        import traceback
        print(traceback.format_exc())
        return "unauthorized"
