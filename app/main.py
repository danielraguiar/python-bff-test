from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.database.database import SessionLocal, engine
from app.models.models import Base, UserData, AdminData
import asyncio

Base.metadata.create_all(bind=engine)

app = FastAPI()

fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}

BASE_URL = "https://api-onecloud.multicloud.tivit.com/fake"


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def authenticate_user(role: str) -> str:
    async with httpx.AsyncClient() as client:
        user = fake_users_db.get(role)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        params = {"username": user["username"], "password": user["password"]}

        try:
            response = await client.get(f"{BASE_URL}/token", params=params)
            response.raise_for_status()
            return response.json()["access_token"]
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")
        except (KeyError, ValueError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid token response: {str(e)}")


@app.get("/health")
async def health_check():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.get("/user")
async def get_user_data(db: Session = Depends(get_db)):
    try:
        token = await authenticate_user("user")
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/user", headers=headers)
            response.raise_for_status()

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
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to fetch user data: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/admin")
async def get_admin_data(db: Session = Depends(get_db)):
    try:
        token = await authenticate_user("admin")
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/admin", headers=headers)
            response.raise_for_status()

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
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to fetch admin data: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")