import uvicorn
import bcrypt
from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel
from fastapi import HTTPException
from enum import Enum

import time
from typing import Dict
from dotenv import load_dotenv, dotenv_values
import jwt

from app.model import User, UserInformation, UserLogin, OrderSchema
from app.auth_handler import signJWT
from app.auth_bearer import JWTBearer

app = FastAPI()
users =[]

from fastapi import FastAPI, Body, HTTPException
import bcrypt
from app.model import User, UserLogin
from app.auth_handler import signJWT, sign_refresh_token
from app.database import conn, config
from sqlalchemy.sql import text

app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Selamat datang!"}


secret_pass = config["HASH-PASS"]

def hash_password(password) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

@app.post("/user/signup", tags=["user"])
async def create_user(user: User):
    if (len(user.username) < 5 or len(user.username) > 16):
        raise HTTPException(status_code=500, detail="username does not fulfill the requirements")
        return
    if (len(user.password) < 8 or len(user.password) > 25):
        raise HTTPException(status_code=500, detail="Password does not fulfill the requirements")
        return
    data = {"username": user.username, "password": hash_password(user.password), "name": user.name, "coins":1000}
    statement = text("""INSERT INTO users(username,password,name, coins) VALUES(:username, :password, :name, :coins)""")
    try:
        conn.execute(statement, **data)
        for row in conn.execute(text("SELECT id from users where username=:username"),{"username": user.username}):
            return {
                "username": user.username,
                "id": row[0],
                "token": signJWT(row[0], user.username)
            }
        raise HTTPException(status_code=600, detail="Internal Server Error")
    except:
        raise HTTPException(status_code=505, detail="Username not unique")

def validate_password(password, hashed) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLogin):
    query = text("""SELECT * FROM users WHERE username=:uname""");
    try :
        result = conn.execute(query, {"uname": user.username})
        for row in result:
            print(result)
            if row[1] == user.username and validate_password(password=user.password, hashed=row[2]):
                return {
                    "username": user.username,
                    "id": row[0],
                    "token": signJWT(row[0], user.username),
                }
        print(result)
    except:
        print("error")
    raise HTTPException(status_code=404, detail="User Not Found")



# @app.get("/users", tags=["users"])
# async def get_users() -> dict:
#     return { "data": users }

# @app.post("/user/signup", tags=["user"]) #Without database
# async def create_user(user: UserSche = Body(...)):
#     for u in users:
#         if (u.email == user.email):
#             raise HTTPException(status_code=400, detail="Username already taken!")
#     users.append(user)
#     return signJWT(user.email)

# def check_user(data: UserLoginSchema):
#     for user in users:
#         if user.email == data.email and user.password == data.password:
#             return True
#     return False

# @app.post("/user/login", tags=["user"])
# async def user_login(user: UserLoginSchema = Body(...)):
#     if check_user(user):
#         return signJWT(user.email)
#     else:
#         raise HTTPException(status_code=401, detail="Wrong username or password!")



# Paket = Enum('Paket', ['Reguler', 'DeepClean', 'Unyellowing'])



order_list = []


@app.post("/order")
async def add_order(model: OrderSchema):
    if (model.paket == "Reguler"):
        order_list.append(model)
        return {"message": "Order berhasil dilakukan."}
    elif (model.paket == "Deep Clean"):
        order_list.append(model)
        return {"message": "Order berhasil dilakukan."}
    elif (model.paket == "Unyellowing"):
        order_list.append(model)
        return {"message": "Order berhasil dilakukan."}
    else:
        return{"message": "Input paket salah!"}
    

@app.get("/orderstatus", dependencies=[Depends(JWTBearer())])
async def get_order():
    return {"Order": order_list}


# @app.get("/orderstatus/{id}")
# async def get_order(id: int):
#     for order in order_list:
#         print(order["id"])
#         if id == order["id"]:
#             return {"Order": order_list[id]}
#     raise HTTPException(status_code=404, detail="Item not found")
# 


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")
