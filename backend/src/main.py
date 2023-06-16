from fastapi import FastAPI
from database import db

app = FastAPI()


@app.get("/")
async def root():
    doc_ref = db.collection("snippets").document("LATTlgOcqCFzKag56vdB")

    doc = doc_ref.get()
    if doc.exists:
        doc_dict = doc.to_dict()
        print(f"Document data: {doc_dict}")
        return doc_dict
    else:
        print("No such document!")
    return doc
