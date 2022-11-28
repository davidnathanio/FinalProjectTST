import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel
from fastapi import HTTPException
from enum import Enum


from app.model import UserSchema, UserLoginSchema
from app.auth import signJWT

app = FastAPI()

users =[]

@app.get("/users", tags=["users"])
async def get_userss() -> dict:
    return { "data": users }

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    for u in users:
        if (u.email == user.email):
            raise HTTPException(status_code=400, detail="Email already taken!")
    users.append(user) # sementara
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=401, detail="Wrong username or password!")




# Paket = Enum('Paket', ['Reguler', 'DeepClean', 'Unyellowing'])

class order(BaseModel):
    id: int
    nama: str
    alamat: str
    sepatu: str
    paket: str

order_list = []


@app.post("/order")
async def add_order(model: order):
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
    

@app.get("/orderstatus")
async def get_order():
    return {"Order": order_list}

''' @app.get("/orderstatus/{id}")
async def get_order(id: int):
    for order in order_list:
        print(order["id"])
        if id == order["id"]:
            return {"Order": order_list[id]}
    raise HTTPException(status_code=404, detail="Item not found") '''

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")
