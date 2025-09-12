from bson import ObjectId

# CRUD для коллекции (например, "users")
async def create_document(db, collection_name: str, data: dict):
    collection = db[collection_name]
    validated = UserDocument(**data)  # Валидация
    result = await collection.insert_one(validated.dict(exclude_unset=True))
    return str(result.inserted_id)

async def read_document(db, collection_name: str, doc_id: str):
    collection = db[collection_name]
    result = await collection.find_one({"_id": ObjectId(doc_id)})
    return result

async def update_document(db, collection_name: str, doc_id: str, updates: dict):
    collection = db[collection_name]
    result = await collection.update_one({"_id": ObjectId(doc_id)}, {"$set": updates})
    return result.modified_count > 0

async def delete_document(db, collection_name: str, doc_id: str):
    collection = db[collection_name]
    result = await collection.delete_one({"_id": ObjectId(doc_id)})
    return result.deleted_count > 0

# Пример в FastAPI
from fastapi import FastAPI, Depends

app = FastAPI()

@app.post("/users/")
async def add_user(user: UserDocument, db = Depends(get_mongo_db)):
    user_id = await create_document(db, "users", user.dict())
    return {"id": user_id}