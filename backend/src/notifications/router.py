from fastapi import APIRouter, HTTPException, status
from database import db
from datetime import datetime
from notifications.models import (
  NotificationBase, NotificationGet, NotificationUpdate
)

router = APIRouter()


# Get all notifications
@router.get(
  "/notifications",
  response_model=list[NotificationGet],
  tags=["notifications"])
async def get_all_notifications():

    notifications_ref = db.collection("notifications")
    query = notifications_ref
    docs = query.stream()
    doc_list = list(docs)

    if len(doc_list) == 0:
        raise HTTPException(status_code=404, detail="Notifications not found.")

    notifications = []
    for doc in doc_list:
        notification = doc.to_dict()
        notification["id"] = doc.id
        notifications.append(notification)
    return notifications


# Get one notification by id
@router.get(
  "/notifications/{id}",
  response_model=NotificationGet,
  tags=["notifications"]
  )
async def get_notification(id: str):
    doc_ref = db.collection("notifications").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Notification not found.")

    notification = doc.to_dict()
    notification["id"] = id
    return notification


# Create a notification
@router.post(
    "/notifications/",
    status_code=status.HTTP_201_CREATED,
    response_model=NotificationGet,
    tags=["notifications"]
    )
async def create_notification(notificationCreate: NotificationBase):
    try:
        notificationCreate.createdAt = datetime.utcnow()
        create_time, doc_ref = db.collection("notifications").add(
            notificationCreate.dict()
        )
        new_notification = NotificationGet(
          id=doc_ref.id,
          **notificationCreate.dict()
        )
        return new_notification

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding notification: {str(e)}"
        )


# Delete a notification by id
@router.delete(
  "/notifications/{id}",
  response_model=NotificationGet,
  tags=["notifications"]
  )
async def delete_notification(id: str):
    try:
        doc_ref = db.collection("notifications").document(id)
        notification_to_delete = doc_ref.get().to_dict()
        doc_ref.delete()
        deleted_notification = NotificationGet(
          id=doc_ref.id,
          **notification_to_delete
        )
        return deleted_notification

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting notification: {str(e)}"
        )


# Update a notification by id
@router.put(
  "/notifications/{id}",
  response_model=NotificationGet,
  tags=["notifications"]
)
async def update_notification(id: str, notificationUpdate: NotificationUpdate):
    try:
        doc_ref = db.collection("notifications").document(id)
        original_notification_data = doc_ref.get().to_dict()
        original_notification_model = NotificationUpdate(
          **original_notification_data
        )
        update_data = notificationUpdate.dict(exclude_unset=True)
        updated_notification = original_notification_model.copy(
          update=update_data
        )
        updated_notification.updatedAt = datetime.utcnow()
        doc_ref.update(updated_notification.dict())

        updated_doc = doc_ref.get()
        final_notification = updated_doc.to_dict()
        final_notification["id"] = id

        return final_notification

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating notification: {str(e)}"
        )
