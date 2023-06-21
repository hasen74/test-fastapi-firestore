from fastapi import APIRouter, HTTPException, status
from database import db
from datetime import datetime
from languages.models import LanguageBase, LanguageGet, LanguageUpdate

router = APIRouter()


# Get all languages
@router.get("/languages", response_model=list[LanguageGet], tags=["languages"])
async def get_all_languages():

    languages_ref = db.collection("languages")
    query = languages_ref
    docs = query.stream()
    doc_list = list(docs)

    if len(doc_list) == 0:
        raise HTTPException(status_code=404, detail="Languages not found.")

    languages = []
    for doc in doc_list:
        language = doc.to_dict()
        language["id"] = doc.id
        languages.append(language)
    return languages


# Get one language by id
@router.get("/languages/{id}", response_model=LanguageGet, tags=["languages"])
async def get_language(id: str):
    doc_ref = db.collection("languages").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Language not found.")

    language = doc.to_dict()
    language["id"] = id
    return language


# Create a language
@router.post(
    "/languages/",
    status_code=status.HTTP_201_CREATED,
    response_model=LanguageGet,
    tags=["languages"]
    )
async def create_language(languageCreate: LanguageBase):
    try:
        languageCreate.createdAt = datetime.utcnow()
        create_time, doc_ref = db.collection("languages").add(
            languageCreate.dict()
        )
        new_language = LanguageGet(id=doc_ref.id, **languageCreate.dict())
        return new_language

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding language: {str(e)}"
        )


# Delete a language by id
@router.delete(
  "/languages/{id}",
  response_model=LanguageGet,
  tags=["languages"]
  )
async def delete_language(id: str):
    try:
        doc_ref = db.collection("languages").document(id)
        language_to_delete = doc_ref.get().to_dict()
        doc_ref.delete()
        deleted_language = LanguageGet(id=doc_ref.id, **language_to_delete)
        return deleted_language

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting language: {str(e)}"
        )


# Update a language by id
@router.put("/languages/{id}", response_model=LanguageGet, tags=["languages"])
async def update_language(id: str, languageUpdate: LanguageUpdate):
    try:
        doc_ref = db.collection("languages").document(id)
        original_language_data = doc_ref.get().to_dict()
        original_language_model = LanguageUpdate(**original_language_data)
        update_data = languageUpdate.dict(exclude_unset=True)
        updated_language = original_language_model.copy(update=update_data)
        updated_language.updatedAt = datetime.utcnow()
        doc_ref.update(updated_language.dict())

        updated_doc = doc_ref.get()
        final_language = updated_doc.to_dict()
        final_language["id"] = id

        return final_language

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating language: {str(e)}"
        )
