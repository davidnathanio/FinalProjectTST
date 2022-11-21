from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from enum import Enum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Final Project TST.", "nama": "David Nathanio Gabriel Siahaan", "NIM": "18220089"}

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


