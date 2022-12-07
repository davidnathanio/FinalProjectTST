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
   

class OrderSchema(BaseModel):
    id: Optional[int] = 0
    nama: str
    alamat: str
    sepatu: str
    warna: str
    paket: OrderType

    class Config:
        schema_extra = {
            "contoh input": {
                "nama" : "Peter Griffin",
                "alamat" : "Jalan Cisitu Elok No.7",
                "sepatu" : "Nike Court Vision Low",
                "warna" : "Putih Biru",
                "paket" : "Reguler"
            }
        }