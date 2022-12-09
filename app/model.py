from pydantic import BaseModel
from enum import Enum
from typing import Optional

class User(BaseModel):
    username: str
    name:str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInformation:
    username: str
    name: str
    coins: int

class OrderType(str, Enum):
    reguler = "Reguler"
    deepclean = "Deep Clean" 
    unyellowing = "Unyellowing"
    repaint = "Repaint"

class PriceList(BaseModel):
    paket: str
    harga: int

class Status(BaseModel):
    id: int
    status: str
   
class OrderSchema(BaseModel):
    id: Optional[int] = 0
    nama: str
    jalan: str
    kota: str
    sepatu: str
    warna: str
    paket: OrderType
    status: Optional[str] = "Dalam proses"

    class Config:
        schema_extra = {
            "contoh input": {
                "nama" : "Peter Griffin",
                "jalan" : "Jalan Cisitu Indah VI",
                "kota" : "Bandung",
                "sepatu" : "Nike Court Vision Low",
                "warna" : "Putih Biru",
                "paket" : "Reguler"
            }
        }