from sqlite3 import IntegrityError
from fastapi import FastAPI,status,HTTPException
from models import UserCreate,User,UserTortoise
from passwords import get_password_hash
import uvicorn


app = FastAPI()

@app.post("/register",status_code=status.HTTP_201_CREATED)
async def createUser(user: UserCreate) -> User:
    new_pass = get_password_hash(user.password)

    try:
        user_tortoise = await UserTortoise.create(**user.dict(),hashed_password= new_pass)
    except IntegrityError:
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")

    return User.from_orm(user_tortoise)       



if __name__ == "__main__":
    uvicorn.run(app,reload=True)