import uvicorn
import bcrypt
from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi import HTTPException
from sqlalchemy import exc

import time
from typing import Dict, List
from dotenv import load_dotenv, dotenv_values

from app.model import User, UserLogin, OrderSchema, PriceList, OrderType, Status
from app.auth_handler import signJWT
from app.auth_bearer import JWTBearer
from app.database import conn, config
from app.url_handler import URLrey
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
    if (len(user.username) < 4):
        raise HTTPException(status_code=400, detail="username minimal 4 karakter")
    if (len(user.password) < 8):
        raise HTTPException(status_code=400, detail="Password minimal 8 karakter")
    try:   
        data = {"username": user.username, "password": hash_password(user.password), "name": user.name}
        statement = text("""INSERT INTO users(username, password, fullName) VALUES(:username, :password, :name)""")
        conn.execute(statement, **data)
        for row in conn.execute(text("SELECT id from users where username=:username"),{"username": user.username}):
            return {
                "username": user.username,
                "id": row[0],
                "token": signJWT(row[0], user.username)
            }
    except exc.IntegrityError: 
        raise HTTPException(status_code=400, detail="Username sudah ada, silahkan pakai username lain!")
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
            if row[1] == user.username and validate_password(password=user.password, hashed=row[2]):
                return {
                    "username": user.username,
                    "id": row[0],
                    "token": signJWT(row[0], user.username),
                }
    except:
        print("error")
    raise HTTPException(status_code=404, detail="Username atau password salah!")



@app.get("/getlistharga", tags=["harga"])
async def get_harga() -> Dict:
    hasil = {}
    for row in conn.execute(text("""SELECT paket, harga FROM hargacuci """)):
        hasil[row[0]] = row[1]
    return hasil

@app.put("/setlistharga", tags=["harga"], dependencies=[Depends(JWTBearer())])
async def set_harga(pricelist: PriceList):
    if (pricelist.paket == "Reguler" or pricelist.paket == "Deep Clean" or pricelist.paket == "Unyellowing" or pricelist.paket == "Repaint"):
        data = {"paket": pricelist.paket, "harga": pricelist.harga}
        statement = text("""UPDATE hargacuci SET harga = :harga WHERE paket = :paket""")
        conn.execute(statement, **data)
        return {"Message": "Perubahan harga berhasil!"}
    else:
        raise HTTPException (status_code=400, detail="Paket tidak sesuai!")

@app.post("/addorder", tags=["order"])
async def add_order(order: OrderSchema):
    #Memanggil API Rey untuk mendapatkan informasi ongkir dan waktu perjalanan
    order.id = conn.execute(text('''select count (*) from orderCuci;''')).scalar() + 1
    data = {"jalan": order.jalan, "kota": order.kota}
    for row in conn.execute(text("""SELECT jalan, kota FROM alamat""")):
        rey = URLrey()
        hasil = rey.getReyHarga("Jalan Dago Asri No.6", "Bandung", order.nama, order.jalan, order.kota)

    #Penentuan Waktu Cuci
    if order.paket == OrderType.reguler:
        waktu_cuci = 60
    elif order.paket == OrderType.deepclean:
        waktu_cuci = 120
    elif order.paket == OrderType.unyellowing:
        waktu_cuci = 150
    elif order.paket == OrderType.repaint:
        waktu_cuci = 210
    
    #Mendapatkan Harga
    harga = {}
    for row in conn.execute(text("""SELECT paket, harga FROM hargacuci""")):
        harga[row[0]] = row[1]
    if order.paket == OrderType.reguler:
        hargacuci = harga['reguler']
    elif order.paket == OrderType.deepclean:
        hargacuci = harga['deepclean']
    elif order.paket == OrderType.unyellowing:
        hargacuci = harga['unyellowing']
    elif order.paket == OrderType.repaint:
        hargacuci = harga['repaint']
    

    #Memasukkan ke Database
    final = hasil.json()
    data = {"id": order.id, "nama": order.nama, "notelp" : order.notelp, "jalan": order.jalan, "kota": order.kota, "sepatu": order.sepatu, "warna": order.warna, "paket": order.paket, "hargacuci": hargacuci, "ongkir": final['priceRupiah'], "waktuCuciMenit": waktu_cuci, "waktuKirimDetik": final['drivingTimeSeconds'], "status": order.status }
    statement = text("""INSERT INTO orderCuci(id, nama, notelp, jalan, kota, sepatu, warna, paket, hargacuci, ongkir, waktuCuciMenit, waktuKirimDetik, status) VALUES(:id, :nama, :notelp, :jalan, :kota, :sepatu, :warna, :paket, :hargacuci, :ongkir, :waktuCuciMenit, :waktuKirimDetik, :status)""")
    conn.execute(statement, **data)
    
    return {
        "Message" : "Pesanan berhasil!",
        "ID Pesanan" : order.id,
        }

@app.get("/orderstatus",  tags=["order"], dependencies=[Depends(JWTBearer())])
async def get_order():
    hasil = []
    for row in conn.execute(text("""SELECT * FROM orderCuci""")):
        hasil.append(
            row
        )
    return hasil

@app.get("/orderstatus/{id}", tags=["order"])
async def get_order_id(id: int):
    hasil = []
    for row in conn.execute(text("""SELECT *, SUM(hargacuci + ongkir) as biayaTotal FROM orderCuci WHERE id = :id"""), {"id": id}):
        hasil.append(
            row
        )
    return hasil

@app.put("/changestatus", tags=["order"])
async def change_status(status: Status):
    try:
        data = {"id": status.id, "status": status.status}
        statement = text("""UPDATE orderCuci SET status = :status WHERE id = :id""")
        result= conn.execute(statement, **data)
        if result.rowcount < 1:
            raise HTTPException (status_code=400, detail="ID tidak sesuai!")
        return {"Message": "Perubahan status berhasil!"}
    except:
        raise HTTPException (status_code=400, detail="ID tidak sesuai!")


@app.get("/order_identity", tags=["misc"])
async def get_order_identity():
    hasil = []
    for row in conn.execute(text("""SELECT DISTICT nama, notelp FROM orderCuci""")):
        hasil.append(
            row
        )
    return hasil


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")
