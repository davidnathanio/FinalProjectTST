import uvicorn
import bcrypt
from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi import HTTPException

import time
from typing import Dict, List
from dotenv import load_dotenv, dotenv_values

from app.model import User, UserLogin, OrderSchema, PriceList, OrderType
from app.auth_handler import signJWT
from app.auth_bearer import JWTBearer
from app.database import conn, config
from app.url_handler import URLrey
from sqlalchemy.sql import text

app = FastAPI()
users =[]



app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Selamat datang!"}


secret_pass = config["HASH-PASS"]

def hash_password(password) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

@app.post("/user/signup", tags=["user"])
async def create_user(user: User):
    if (len(user.username) < 4):
        raise HTTPException(status_code=500, detail="username minimal 4 karakter")
        return
    if (len(user.password) < 8):
        raise HTTPException(status_code=500, detail="Password minimal 8 karakter")
        return
    data = {"username": user.username, "password": hash_password(user.password), "name": user.name}
    statement = text("""INSERT INTO users(username, password, fullName) VALUES(:username, :password, :name)""")
    conn.execute(statement, **data)
    try:
        for row in conn.execute(text("SELECT id from users where username=:username"),{"username": user.username}):
            return {
                "username": user.username,
                "id": row[0],
                "token": signJWT(row[0], user.username)
            }
        raise HTTPException(status_code=600, detail="Pilih username lain!")
    except:
        raise HTTPException(status_code=505, detail="Signup Error")

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



@app.get("/getlistharga", tags=["main"])
async def get_harga() -> Dict:
    hasil = {}
    for row in conn.execute(text("""SELECT paket, harga FROM hargacuci """)):
        hasil[row[0]] = row[1]
    return hasil

@app.put("/setlistharga", tags=["main"])
async def set_harga(pricelist: PriceList):
    data = {"paket": pricelist.paket, "harga": pricelist.harga}
    statement = text("""UPDATE hargacuci SET harga = :harga WHERE paket = :paket""")
    conn.execute(statement, **data)
    return {"Message": "Perubahan berhasil!"}

@app.post("/order", tags=["main"])
async def add_order(order: OrderSchema):
    count = 0
    order.id = conn.execute(text('''select count (*) from orders;''')).scalar() + 1
    data = {"jalan": order.jalan, "kota": order.kota}
    for row in conn.execute(text("""SELECT jalan, kota FROM alamat""")):
        rey = URLrey()
        hasil = rey.getReyHarga("Jalan Dago Asri No.6", "Bandung", order.jalan, order.kota)

    #Penentuan Waktu Cuci
    if order.paket == OrderType.reguler:
        waktu_cuci = 60
    if order.paket == OrderType.deepclean:
        waktu_cuci = 120
    if order.paket == OrderType.unyellowing:
        waktu_cuci = 150
    if order.paket == OrderType.repaint:
        waktu_cuci = 210
    
    #Mendapatkan Harga
    harga = {}
    for row in conn.execute(text("""SELECT paket, harga FROM hargacuci """)):
        harga[row[0]] = row[1]
    if order.paket == OrderType.reguler:
        hargacuci = harga['reguler']
    if order.paket == OrderType.deepclean:
        hargacuci = harga['deepclean']
    if order.paket == OrderType.unyellowing:
        hargacuci = harga['unyellowing']
    if order.paket == OrderType.repaint:
        hargacuci = harga['repaint']



    final = hasil.json()
    data = {"id": order.id, "nama": order.nama, "jalan": order.jalan, "kota": order.kota, "sepatu": order.sepatu, "warna": order.warna, "paket": order.paket, "harga": hargacuci, "ongkir": final['priceRupiah'], "waktuCuciMenit": waktu_cuci, "waktu_kirim": final['drivingTimeSeconds'], }
    statement = text("""INSERT INTO orders(id, nama, jalan, kota, sepatu, warna, paket, harga, ongkir, waktuCuciMenit, waktu_kirim) VALUES(:id, :nama, :jalan, :kota, :sepatu, :warna, :paket, :harga, :ongkir, :waktuCuciMenit, :waktu_kirim)""")
    conn.execute(statement, **data)
    
    return {
        "Message" : "Pesanan berhasil!",
        "ID Pesanan" : order.id,
        }

 


@app.get("/orderstatus",  tags=["main"])
async def get_order():
    hasil = {}
    for row in conn.execute(text("""SELECT id, nama, jalan, kota FROM orders""")):
        hasil[row[0]] = row[1]
    return hasil


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
