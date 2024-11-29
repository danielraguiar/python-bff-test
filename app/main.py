from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.database.database import SessionLocal, engine
from app.models.models import Base, UserData, AdminData

Base.metadata.create_all(bind=engine)

app = FastAPI()

fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}

BASE_URL = "https://api-onecloud.multicloud.tivit.com/fake"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(role: str) -> str:
    user = fake_users_db.get(role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    params = {"username": user["username"], "password": user["password"]}
    response = httpx.get(f"{BASE_URL}/token", params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return response.json()["access_token"]


@app.get("/health")
async def health_check():
    response = httpx.get(f"{BASE_URL}/health")
    return response.json()


@app.get("/user")
async def get_user_data(db: Session = Depends(get_db)):
    token = authenticate_user("user")
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(f"{BASE_URL}/user", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user data")

    data = response.json()["data"]
    for purchase in data["purchases"]:
        user_data = UserData(
            name=data["name"],
            email=data["email"],
            item=purchase["item"],
            price=purchase["price"]
        )
        db.add(user_data)
    db.commit()
    return data


@app.get("/admin")
async def get_admin_data(db: Session = Depends(get_db)):
    token = authenticate_user("admin")
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(f"{BASE_URL}/admin", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch admin data")

    data = response.json()["data"]
    for report in data["reports"]:
        admin_data = AdminData(
            name=data["name"],
            email=data["email"],
            title=report["title"],
            status=report["status"]
        )
        db.add(admin_data)
    db.commit()
    return data