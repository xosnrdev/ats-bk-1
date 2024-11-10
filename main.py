from fastapi import FastAPI, Request, status, HTTPException
from pydantic import BaseModel, conint, EmailStr, confloat, field_validator
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

users_db = []


class User(BaseModel):
    first_name: str
    last_name: str
    age: conint(gt=0)
    email: EmailStr
    height: confloat(gt=0)

    @field_validator("email")
    def email_to_lower(cls, v):
        return v.lower()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} processed in {process_time:.4f} seconds")
    return response


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    for u in users_db:
        if u["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

    users_db.append(user.model_dump())
    return {"message": "User created successfully", "user": user}
